# Measurement and pilot plan

No production event log, costs or customer survey results were supplied. All metrics below are **proposed definitions**. Baselines, targets and benefits remain unmeasured.

## Minimum event data

Use one stable `case_id` and an immutable `event_id`. Record `event_type`, timestamp with timezone, previous/new state, responsible role, priority at the time, issue category and the related escalation or partner reference. For deadline changes, retain `due_at`, policy/calendar version and the reason for the change. Keep the original intake timestamp when a case is reopened; record the reopen event separately.

Suggested events: `case_received`, `intake_completed`, `client_wait_started`, `client_wait_ended`, `owner_assigned`, `priority_changed`, `due_date_set`, `escalation_sent`, `escalation_acknowledged`, `resolution_completed`, `customer_confirmed`, `feedback_requested`, `feedback_received`, `case_closed`, `case_reopened`, `case_cancelled` and `sync_failed`.

Calculate intervals in a common timezone; display local time to users. Working-day metrics require an explicitly agreed business calendar. Preserve missing values rather than filling them with invented timestamps.

## KPI dictionary

| Metric | Proposed definition | Interpretation and guardrail |
| --- | --- | --- |
| Intake completeness | Cases with required routing fields complete at first submission / eligible submitted cases | Also measure assisted intake and form abandonment |
| Resolution cycle time | `resolution_completed - case_received` | Report median and p90 by priority/type; show unresolved age separately |
| Time awaiting client | Sum of non-overlapping client-wait intervals per case | Report separately from active handling; do not subtract it from contractual SLAs without policy approval |
| Deadline compliance | Cases resolved by their policy-defined due date / eligible cases whose due date falls in the reporting window | Include overdue open cases; show missing due dates as a separate quality issue; preserve escalation history |
| Escalation acknowledgement time | `escalation_acknowledged - escalation_sent` per escalation | Report unacknowledged count and age; never silently drop them |
| Reopen rate | Cases reopened within an agreed observation window / closed cases with that full follow-up window | Exclude immature cohorts from the denominator; show cancellations separately |
| Update effort | Observed staff minutes spent recording a case change across all required views | Sample consistently; separate task time from elapsed waiting |
| Conflicting-record rate | Sampled cases with inconsistent status across authoritative views / sampled cases | Define authoritative fields and sampling method before comparison |
| Feedback response rate | Feedback received within an agreed response window / eligible requests with the full window elapsed | Non-response is not positive feedback; avoid duplicate reminders in the denominator |
| Closure-to-review lag | `internal_review_completed - resolution_completed` | Include unresolved review backlog and avoid conflating it with resolution speed |
| Improvement action completion | Actions completed by their due date / actions due in the period | Completion alone is insufficient; review the action's measured effect |
| Repeat-issue rate | Repeat cases under an agreed shipment/customer/category matching rule / eligible cases | Matching rules, privacy access and observation period require agreement |

If feedback includes a satisfaction scale, define the scale and report response count and rate with the score. A case closure event is not a satisfaction measurement.

## Pilot sequence

1. **Agree scope and definitions.** Select one team and a manageable issue segment; confirm owners, priority rules, working calendars and mandatory closure controls.
2. **Validate the data.** Reconcile case counts; check duplicate events, impossible timestamp order, missing priorities and incomplete wait intervals. Investigate failures before calculating metrics.
3. **Establish the baseline.** Observe the current process over a period agreed with the process owner. Set the required case volume and duration before looking at results.
4. **Introduce a bounded change.** Begin with intake ownership, due-date visibility or feedback separation. Record rollout dates and avoid combining unrelated changes in the same evaluation.
5. **Compare comparable cases.** Use the same definitions, priority segments and observation windows. Where practical, use a contemporaneous comparison group; document case-mix and staffing changes.
6. **Decide using guardrails.** Agree targets after baseline measurement. Assess resolution time alongside reopen rate, complaints, compliance exceptions and staff workload. Expand only when the agreed outcomes and quality controls are met.

## Benefit calculation template

For an update-effort pilot:

`estimated staff hours avoided = eligible case changes × measured mean minutes avoided per change / 60`

Use observed effort from comparable samples and report uncertainty. Multiplying by a documented loaded hourly rate estimates released capacity value; it does not establish cash savings. Do not count waiting-time reduction as staff labour savings or add overlapping benefits twice.
