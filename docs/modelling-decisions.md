# Modelling decisions

These notes explain constructs present in the supplied model and their business purpose. They are a retrospective interpretation of the artifact, not a claim that every original choice has been validated.

| Design area | Source-model representation | Business purpose |
| --- | --- | --- |
| Process boundary | SwiftCargo white-box participant with three external black-box participants | Show internal accountability without inventing a partner's internal workflow |
| Responsibilities | Functional lanes and nested Response Team lanes | Make ownership and internal hand-offs visible |
| Abstraction | Eight regular sub-processes, nine diagrams, one expanded ad-hoc sub-process | Let readers move between the case lifecycle and detailed handling |
| Priority routing | Exclusive gateways in `Assess and resolve issue` | Route medium/low, high and critical cases through different handling paths |
| Waiting for alternatives | Four event-based gateways | Represent races such as incoming client information versus a timeout |
| Interruption | Cancellation message boundary on `Assess and resolve issue`; timer boundary on critical recovery task | Show work being interrupted by an external cancellation or elapsed recovery time |
| External communication | Labelled message flows between participant pools | Distinguish communication with outside parties from sequence flow within the organisation |
| Variable assessment order | Ad-hoc `Assess complex solution` | Represent assessment, schedule review and resource checking in varying sequential order |
| Multiple participants | Multi-instance marker on the Claims Officer participation task in close-out | Represent one participation instance per officer |
| Data context | Data objects/references and data associations | Connect work with case-related information |
| Assumptions | Text annotations in the high-priority and close-out details | Expose interpretation where the narrative is incomplete |

## Main decomposition

- SwiftCargo main collaboration
  - Confirm issue details
  - Assess and resolve issue
    - Resolve standard issue
    - Resolve critical issue
    - Resolve high-priority issue
      - Assess complex solution, expanded ad-hoc block on the same diagram
  - Collect feedback and close out
    - Conduct Claims Close-out Meeting
  - Conduct monthly review

## Choices to revisit

The monthly review is a separate timer-started path in the main process. A production design should first decide whether review is a schedule independent of any one case or a repeated action within a case lifecycle. That decision affects the BPMN scope.

Timer labels express the business intent, but most timer definitions contain no formal duration; the monthly expression is descriptive text. The model is a design artifact rather than a configured workflow engine package.

The ad-hoc block permits variable sequential assessment activities. Its annotation discusses repetition, but an executable completion condition and a verified repetition policy are not established by this export. See [model review](model-review.md).
