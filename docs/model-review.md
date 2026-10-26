# Review of the preserved AS-IS model

## Review scope

This review covers the supplied XML, its diagram definitions and comparison with the local case brief and teaching guide. It is not a grade, a full BPMN conformance audit or a fresh native Signavio check. The original model is preserved so that its strengths and limitations can be inspected directly.

## Findings to carry into the next revision

| Finding | File evidence / implication | Next action |
| --- | --- | --- |
| One reminder message flow has no endpoints | `Feedback reminder`, ID `sid-BD9C3D9C-0D35-40CA-9B36-1BAD260FFE0B`, has neither `sourceRef` nor `targetRef`; the renderer flags and omits it | Connect the intended reminder throw event and client participant in a reviewed model revision |
| Timer configuration is incomplete | Six timer definitions exist. Five have no expression; the monthly timer uses the descriptive `timeDuration` value `every month` | Agree the business calendar and configure supported timer expressions before execution |
| Standard handling deadline is not explicitly represented by a timer | The standard-resolution sub-process has no timer, although the case specifies a one-week resolution timeframe | Decide with the process owner whether this is a monitored target or an interrupting escalation rule, then model it explicitly |
| Monthly review scope needs clarification | Two top-level starts exist: issue notification and a monthly timer | Decide whether monthly governance is independent of a case or tied to an active case scope |
| Ad-hoc repetition is described rather than fully specified | `Assess complex solution` has three tasks and an annotation about repetition; it has no explicit completion condition or loop marker | Agree completion/repetition semantics and test the allowed paths |
| The feedback wait can continue indefinitely | The close-out sub-process returns from weekly reminder to the feedback wait | Consider the separately proposed bounded follow-up policy; preserve complaint/reopen routes |
| Full native verification remains outstanding | No current Signavio syntax/convention result or execution trace was supplied | Import a review copy, run native checks and preserve revision-specific results |
| Layout needs another readability pass | Main-diagram message labels crowd together; some narrow lane labels and the expanded ad-hoc block overlap in the generated rendering | Tidy a separate review copy and verify it in Signavio; the preserved historical artifact is unchanged |

Some observations are **modelling refinements** needed to express the current process accurately; others are **business redesign proposals** that change policy. Review them separately with the process owner.

## Validation layers

1. **XML and reference inspection:** the repository script checks parseability, ID uniqueness, known reference targets and diagram coverage. Missing flow endpoints are separately reported as source findings; timer expressions require review. A successful `--check` means the selected integrity checks and committed report agree, not that the source is defect-free.
2. **Diagram rendering:** previews show the saved layout through a separate renderer. This can expose presentation issues but does not prove valid token flow.
3. **Native Signavio checks:** require a live workspace and the organisation's modelling conventions; not performed here.
4. **Business walkthrough:** owners should review normal, timeout, cancellation, disagreement, late-reply and escalation paths. Not established by the artifact alone.
5. **Operational pilot:** requires actual event data and agreed guardrails. No measured improvement is claimed.

## Suggested walkthrough scenarios

- Client confirms promptly; a standard issue is resolved and accepted.
- No confirmation arrives within 24 hours, then information arrives during the idle period.
- No information arrives by the two-week deadline.
- A critical recovery exceeds three days and transfers to the recovery partner.
- A loss-adjuster response arrives before five days; a separate case exceeds the deadline.
- The client cancels while assessment or resolution is active.
- The client disputes a standard resolution and requests further investigation.
- Feedback never arrives, or arrives after multiple reminders.

For each scenario, ask who owns the case, which work remains active, what message is sent, how the state changes and what evidence proves the next step can proceed.
