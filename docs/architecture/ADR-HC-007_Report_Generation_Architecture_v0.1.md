# ADR-HC-007 — Report Generation Architecture v0.1

## Status
`PROPOSED — PROJECT OWNER APPROVAL REQUIRED`

## Decision
Reports SHALL be generated from canonical structured session data and linked media, not from transient HMI screen state. Report generation SHALL reside in the local edge/data layer or a dedicated local reporting component.

The report model SHALL support audience-specific sections for farmer, veterinarian, zootechnician, nutritionist and technical service while retaining one canonical underlying treatment record.

Reference/example images SHALL be labeled distinctly from actual-animal evidence. Generated reports SHALL carry document identity, generation timestamp and source session identity.

## MVP
Bench MVP may generate local PDF reports using synthetic/test data only.

## Deferred choices
PDF library, templates, email delivery and external document storage are implementation/architecture details downstream of this ADR.
