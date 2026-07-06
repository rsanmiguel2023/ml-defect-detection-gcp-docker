# Incident Response

## Overview

This document defines the incident response process for the Industrial Defect Detection platform.

The goal is to restore service quickly, communicate clearly, and capture lessons learned after every significant incident.

## Severity Levels

| Severity | Description | Examples |
|---|---|---|
| SEV-1 | Complete service outage or prediction unavailable | API down, all predictions failing |
| SEV-2 | Major degradation or partial outage | High error rate, severe latency, model load failures |
| SEV-3 | Minor degradation or elevated risk | Warning latency, low cache hit rate |
| SEV-4 | Informational or non-urgent issue | Documentation issue, minor alert noise |

## Incident Roles

| Role | Responsibility |
|---|---|
| Incident Lead | Coordinates response and decisions |
| Technical Lead | Investigates and resolves technical issue |
| Communications Lead | Provides updates to stakeholders |
| Scribe | Records timeline and actions |
| Reviewer | Leads post-incident review |

## Response Process

1. Detect and acknowledge the incident.
2. Assign severity.
3. Identify incident lead.
4. Create incident timeline.
5. Stabilize the system.
6. Mitigate user impact.
7. Communicate status.
8. Restore normal operation.
9. Complete post-incident review.

## Communication Cadence

| Severity | Update Frequency |
|---|---|
| SEV-1 | Every 15 minutes |
| SEV-2 | Every 30 minutes |
| SEV-3 | Every 2 hours |
| SEV-4 | As needed |

## Initial Triage Checklist

- Is `/health` responding?
- Is `/ready` responding?
- Are predictions failing?
- Is the issue limited to one framework, category, or version?
- Was there a recent deployment?
- Are Cloud Run instances restarting?
- Are there model loading errors?
- Is latency above SLO?
- Is error rate above threshold?

## Root Cause Analysis Template

```text
Incident Title:
Date:
Severity:
Duration:
Detected By:
Impacted Service:
User Impact:

Timeline:
- HH:MM Event
- HH:MM Action
- HH:MM Recovery

Root Cause:
Contributing Factors:
Resolution:
What Went Well:
What Could Improve:
Follow-up Actions:
Owner:
Due Date:
```

## Post-Incident Review

A post-incident review should be completed for all SEV-1 and SEV-2 incidents.

The review should be blameless and focused on system improvement.

Required outputs:

- Root cause
- Timeline
- Customer impact
- Mitigation
- Preventive actions
- Monitoring improvements
- Documentation updates

## Follow-Up Action Categories

- Code fix
- Infrastructure change
- Monitoring improvement
- Alert tuning
- Documentation update
- Runbook update
- Security review
- Testing improvement
