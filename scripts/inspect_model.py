#!/usr/bin/env python3
"""Inspect the preserved design artifact; not a BPMN execution/conformance test."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / 'models' / 'swiftcargo-as-is.bpmn'
REPORT = ROOT / 'docs' / 'evidence' / 'model-inventory.json'
B = 'http://www.omg.org/spec/BPMN/20100524/MODEL'
D = 'http://www.omg.org/spec/BPMN/20100524/DI'


def inspect(path: Path) -> dict:
    data = path.read_bytes()
    root = ET.fromstring(data)
    counts = Counter(e.tag.split('}')[-1] for e in root.iter())
    ids = [e.get('id') for e in root.iter() if e.get('id')]
    by_id = {e.get('id'): e for e in root.iter() if e.get('id')}
    errors = []
    findings = []
    duplicates = sorted(k for k, v in Counter(ids).items() if v > 1)
    if duplicates:
        errors.append({'kind': 'duplicate_ids', 'ids': duplicates})
    ref_attributes = {'sourceRef', 'targetRef', 'processRef', 'attachedToRef', 'bpmnElement', 'dataObjectRef', 'default'}
    ref_elements = {'incoming', 'outgoing', 'flowNodeRef', 'sourceRef', 'targetRef', 'dataInputRefs', 'dataOutputRefs', 'inputSetRefs', 'outputSetRefs'}
    for e in root.iter():
        if e.tag in {f'{{{B}}}sequenceFlow', f'{{{B}}}messageFlow'}:
            missing = [key for key in ('sourceRef', 'targetRef') if not e.get(key)]
            if missing:
                findings.append({'kind': 'missing_flow_endpoints', 'id': e.get('id'),
                                 'name': e.get('name'), 'missing': missing})
        refs = [(k, v) for k, v in e.attrib.items() if k in ref_attributes]
        if e.tag.split('}')[-1] in ref_elements and e.text:
            refs += [('text', e.text.strip())]
        for key, value in refs:
            if value not in by_id:
                errors.append({'kind': 'unresolved_reference', 'element': e.get('id'), 'attribute': key, 'target': value})
    diagrams = []
    planes = set()
    for diagram in root.findall(f'{{{D}}}BPMNDiagram'):
        plane = diagram.find(f'{{{D}}}BPMNPlane')
        if plane is None:
            errors.append({'kind': 'missing_plane', 'diagram': diagram.get('id')})
            continue
        target = plane.get('bpmnElement')
        planes.add(target)
        element = by_id.get(target)
        name = 'Main collaboration' if element is not None and element.tag.endswith('collaboration') else (element.get('name') if element is not None else target)
        diagrams.append({'id': diagram.get('id'), 'element': target, 'name': name,
                         'shapes': len(plane.findall(f'{{{D}}}BPMNShape')),
                         'edges': len(plane.findall(f'{{{D}}}BPMNEdge'))})
    for e in root.findall(f'.//{{{B}}}subProcess'):
        if e.get('id') not in planes:
            expanded = any(s.get('bpmnElement') == e.get('id') and s.get('isExpanded') == 'true'
                           for s in root.findall(f'.//{{{D}}}BPMNShape'))
            if not expanded:
                errors.append({'kind': 'missing_subprocess_diagram', 'id': e.get('id'), 'name': e.get('name')})
    parent = {child: e for e in root.iter() for child in e}
    timers = []
    for timer in root.findall(f'.//{{{B}}}timerEventDefinition'):
        event = parent[timer]
        expressions = [{'type': c.tag.split('}')[-1], 'value': (c.text or '').strip()} for c in timer]
        timers.append({'event_id': event.get('id'), 'event': event.get('name'), 'expressions': expressions,
                       'status': 'missing_expression' if not expressions else 'descriptive_expression_requires_review'})
    top = root.find(f'{{{B}}}process')
    top_starts = [{'id': e.get('id'), 'name': e.get('name')} for e in top.findall(f'{{{B}}}startEvent')]
    return {
        'model': path.relative_to(ROOT).as_posix(),
        'sha256': hashlib.sha256(data).hexdigest(),
        'bytes': len(data),
        'exporter': root.get('exporter'),
        'exporter_version': root.get('exporterVersion'),
        'counts': dict(sorted(counts.items())),
        'diagrams': diagrams,
        'top_level_starts': top_starts,
        'timer_review': timers,
        'structural_errors': errors,
        'source_findings_requiring_review': findings,
        'limitations': [
            'Checks are limited to XML, IDs, selected reference types and diagram coverage.',
            'Timer labels and descriptive expressions do not establish executable timer configuration.',
            'No schema conformance, token-flow soundness, native Signavio check or process execution is claimed.',
            'Element counts are not a rubric score or a quality certification.'
        ]
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Refresh the committed inventory JSON')
    parser.add_argument('--check', action='store_true', help='Fail on structural errors or a stale committed inventory')
    args = parser.parse_args()
    report = inspect(MODEL)
    content = json.dumps(report, indent=2, ensure_ascii=False) + '\n'
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(content, encoding='utf-8')
    stale = not REPORT.exists() or REPORT.read_text(encoding='utf-8') != content
    print(f"Model SHA-256: {report['sha256']}")
    print(f"Diagrams: {len(report['diagrams'])}; tasks: {report['counts']['task']}; message flows: {report['counts']['messageFlow']}")
    print(f"Reference/coverage errors: {len(report['structural_errors'])}; source findings: {len(report['source_findings_requiring_review'])}; timer definitions needing review: {len(report['timer_review'])}")
    print('Native Signavio validation and process execution: not performed')
    if report['structural_errors']:
        print(json.dumps(report['structural_errors'], indent=2))
    if report['source_findings_requiring_review']:
        print(json.dumps(report['source_findings_requiring_review'], indent=2))
    if args.check and stale:
        print('Committed inventory is stale; regenerate with --write.', file=sys.stderr)
    return 1 if args.check and (report['structural_errors'] or stale) else 0


if __name__ == '__main__':
    raise SystemExit(main())
