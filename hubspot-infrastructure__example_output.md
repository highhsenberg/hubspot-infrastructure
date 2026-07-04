# Example run

```
$ python crm_pipeline.py --input contacts.csv

=== Lifecycle stage transitions ===

Dana Ruiz <dana@brightpath.io>
  lead -> sql (advanced, score=68)
  Workflow triggered: Assign to AE, create task 'first call within 24h'

Emeka Cole <emeka@northstartech.com>
  subscriber -> lead (advanced, score=35)
  Workflow triggered: Add welcome email sequence

Mia Torres <mia@haloworks.co>
  mql -> customer (advanced, score=92)
  Workflow triggered: Trigger onboarding sequence, notify CS team

Liam Foster <liam@vertexbuild.com>
  sql -> mql (regressed, score=45)
  ! Stalled - no activity in 120 days
  Workflow triggered: Notify marketing, add to nurture-to-sales handoff list

Sofia Almeida <sofia@driftlane.com>
  opportunity -> lead (regressed, score=30)
  ! Stalled - no activity in 200 days
  Workflow triggered: Add welcome email sequence

=== Stage distribution ===

  subscriber   0 contacts (0.0%)
  lead         2 contacts (40.0%)
  mql          1 contacts (20.0%)
  sql          1 contacts (20.0%)
  opportunity  0 contacts (0.0%)
  customer     1 contacts (20.0%)
```

## Why regressions matter

Liam Foster and Sofia Almeida both show something a naive "always move
forward" lifecycle model would hide: their engagement dropped off (120 and
200 days of inactivity) and their current activity score no longer supports
the stage they were previously marked at. Recomputing stage from live
activity data -- rather than only ever moving contacts forward -- surfaces
stalled deals that need a human to re-engage them, instead of quietly
inflating the pipeline with contacts who look further along than they are.
