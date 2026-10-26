# SAP Signavio: tool evidence and workflow

## What the artifact establishes

The source XML identifies its exporter as **Signavio Process Editor** and records exporter version `26.36.0-20260906220451+53486f4`. It contains Signavio extension metadata, one collaboration, the main process, nested sub-processes and nine BPMN diagram planes with layout coordinates.

This supports a portfolio claim of **SAP Signavio BPMN process modelling, hierarchical decomposition and BPMN 2.0 XML export**. The supplied artifact demonstrates use of pools, lanes, message flows, gateways, timers, boundary events, an ad-hoc block, a multi-instance task and annotations.

## Review workflow

The following is a reproduction guide. A fresh native Signavio import and validation were not performed as part of preparing this repository.

1. Download [the BPMN model](../models/swiftcargo-as-is.bpmn).
2. Use an authorised Signavio workspace and import the file as BPMN 2.0 XML. Menu labels can vary by workspace version.
3. Open the main model and inspect all eight regular sub-processes. The expanded ad-hoc block appears within the high-priority diagram.
4. Check participant boundaries, lane ownership, flow endpoints and the cancellation/timeout branches. Review model-wide exceptions as well as the happy paths.
5. Run the workspace's syntax and modelling-convention checks. Record errors, warnings and hints separately, with the model revision and date.
6. Confirm timer and business-calendar policy, then inspect each diagram at a readable scale. Export all relevant diagrams if a full PDF is required.

## Evidence boundaries

| Item | Evidence available |
| --- | --- |
| Modelling tool and export | Verified in the supplied XML metadata |
| BPMN constructs and diagram coverage | Reproducible static inventory |
| Preview rendering | Generated from source layout; see [gallery](model-gallery.md) |
| New import into a live Signavio workspace | Not performed for this portfolio |
| Fresh native syntax/convention check | Not available |
| Process simulation or process mining | Not available |
| SAP S/4HANA configuration, ABAP or ERP integration | Outside the supplied evidence |
| Production workflow execution or measured business impact | Not available |

A rendered preview or well-formed XML alone does not establish semantic correctness or a successful Signavio validation.
