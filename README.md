# HubSpot CRM Infrastructure (lite)

A small, readable model of the three things most "CRM infrastructure" work
actually involves: lifecycle stage management, workflow automation, and
funnel reporting -- built to slot in front of a real HubSpot/Salesforce
instance.

See [`example_output.md`](./example_output.md) for a full run, including a
worked example of why regressions (stalled deals) matter.

## How it works

1. **Lifecycle stage** -- each contact's stage is recomputed from a live
   activity score against fixed thresholds (subscriber -> lead -> mql ->
   sql -> opportunity -> customer), rather than only ever moving contacts
   forward. This surfaces stalled deals instead of hiding them.
2. **Workflow automation** -- whenever a contact's stage changes, a matching
   action fires automatically (assign an owner, create a task, notify a
   team) instead of a rep having to remember to do it.
3. **Funnel reporting** -- a snapshot of how many contacts currently sit in
   each lifecycle stage, with percentages.

## Install

No external dependencies beyond the Python standard library.

## Usage

```bash
python crm_pipeline.py --input contacts.csv
```

## Project structure

```
crm_pipeline.py    -- lifecycle scoring + workflow automation + reporting
contacts.csv        -- 5 example contacts covering advances, a big jump, and two stalls
example_output.md   -- full example run with reasoning
```

## Limitations / next steps

- Stage thresholds are a simple, tunable rubric -- not a trained model.
- This reports a current-state snapshot, not a true time-series funnel;
  logging each transition event (which the workflow trigger already has
  the data for) is the natural next step toward real conversion-rate
  reporting between stages over a date range.
- Workflow "actions" here just print to the console -- wiring them to real
  HubSpot/Slack/task-creation APIs is a drop-in change at the call site.
