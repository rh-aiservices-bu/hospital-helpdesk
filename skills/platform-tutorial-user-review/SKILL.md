---
name: platform-tutorial-user-review
description: "Follow a platform tutorial end-to-end as a regular user with no admin rights, capturing doc-vs-UI mismatches, failures, confusion, and unanswered questions — pairs with rhoai-tutorial-admin-setup"
---

# Review a Platform Tutorial as a Regular User (learner role)

Use for any platform tutorial (RHOAI, Kubernetes, cloud console, SaaS). You are a regular end-user of `<platform>` — `<persona>` — with **no admin rights**. The platform is already installed and configured by an administrator. Follow the tutorial *exactly as written* and report the experience honestly. Pair with the companion skill `rhoai-tutorial-admin-setup` for the install side.

## Inputs (fill every `<placeholder>` before starting)
- Tutorial under review: `<path or URL>`. Multi-page docs site → build and serve it locally, review the **rendered** pages, never the raw source (raw source shows template placeholders and unresolved links that are not real findings).
- Platform UI URL + regular-user credentials in `<creds file>`. Use only regular-user credentials — never admin credentials, even if they sit in the same file.
- Admin handoff note: what the admin pre-provisioned (versions, flags, pre-created resources). Expected state only — a note recounting past failures biases the review toward confirming them.
- Review folder: one unique, git-ignored run folder per review execution — `review/<YYYY-MM-DD>-<slug>/` (append `-2` or `-HHMM` if it already exists) — holding everything the run produces: findings `.md` file(s) at `review/<run>/findings.md`, screenshots at `review/<run>/screens/<module>-<step>-<short-name>.png`, logs. Create it (`mkdir -p`) and add the `.gitignore` entry (`review/`) before the first capture; write nothing review-related outside it.

## Before you start
1. **Check your privilege level matches the tutorial's audience.** More rights than a regular user (admin-only menus, ability to patch cluster resources) → state it in the findings header; permission findings from a privileged account are unreliable and must be labeled untested.
2. **Derive the module list from the tutorial's own navigation** (TOC, index, sidebar) at runtime. No pre-baked module map. Nav defects are findings: module missing from nav, dangling next/prev link, orphaned page, numbering that skips.
3. **Record what the tutorial promises up front**: listed prerequisites, assumed platform state, time estimates. "No duration given anywhere" is itself a finding.

## Work through every module in order, as a learner would
- Alternatives (scripted vs manual, UI vs CLI, optional vs required): take the primary path first, note the alternative exists.
- Optional step: ask whether later modules depend on it — skip once, note downstream breakage, go back and complete if needed. "The docs don't say what this optional step feeds" is a finding either way.

## Capture per step
1. **Instruction vs UI**: where the doc's words differ from what you see (button labels, menus, step order, missing elements). Screenshot every mismatch: `<review-run>/screens/<module>-<step>-<short-name>.png`.
2. **Does it work?** Success/failure per step; on failure capture exact error text (screenshot + copy).
3. **Does it make sense?** Jargon before explanation, assumed knowledge not yet taught, ambiguity ("select Projects" — which dashboard?), references to screens that don't exist.
4. **Complexity**: steps much longer than implied, too many manual fields, beginner-would-give-up spots.
5. **Unanswered questions**: every "how do I...?" the tutorial didn't answer; every missing link, definition, or "why am I doing this?".
6. **Terminology drift**: between tutorial, product UI, and branding. Report which name appears where; never silently adopt one.

## Role boundary
- Everything the user-facing UI lets you do, plus every action the **tutorial itself instructs** (CLI commands, console YAML import, setup scripts), is in scope. Tutorial-instructed actions are never "admin work" — follow them exactly and report what happens.
- Outside the tutorial, anything needing elevated rights (missing flag, missing resource, permission denied): **stop and report it as a question for the admin**, don't work around it. If you work around anyway, the workaround is a finding, not a success.
- Pre-provisioned extras alongside what a tutorial step says to create: note once in the findings header, move on. A step failing from a pre-provisioned conflict → handoff-note/reality mismatch.

## Findings format (append per module — never hold in memory until the end)
```
## Module N — <name>
### Steps that worked
### Steps that failed or mismatched the docs
- [doc quote] vs [what I saw] → [screenshot]
### Confusion / complexity
### Unanswered questions for the admin or the docs authors
```
Overall verdict afterwards:
- Could a first-time user complete this tutorial alone? (yes / with help / no — why)
- Time-to-complete estimate vs what the tutorial implies (no stated duration → say so)
- Top 3 things to fix in the docs, ranked by learner blockage
- Top 3 platform prerequisites missing from the docs' prerequisites section — cross-check against the "Before you start" step 3 list so claimed-but-unverified and missing both surface.

## Expected state (from the admin)
`<paste the admin's handoff checklist here>`. A step failing in a way this list says was pre-configured → mismatch between handoff note and reality, not your error.

## Rules
- Follow the tutorial **in order**; no skipping ahead. A step that only works via something the tutorial didn't say is a finding, not a success.
- Never edit the tutorial's source to make a step pass.
- No outside sources unless a step is truly impossible — then note it, try the most likely alternative, report what you had to do.
- Screenshot everything you'd show a colleague when explaining a problem.
- Be specific: exact button labels, exact error text, exact screenshots.

## Review folder hygiene
- One unique, git-ignored run folder per review execution, under a shared `review/` root: `review/<YYYY-MM-DD>-<slug>/` (append `-2` or `-HHMM` if it already exists). Everything the run generates goes inside it: findings `.md` file(s), `screens/`, logs, transcripts. Create it and ensure the `review/` gitignore entry exists before the first capture.
- Never commit review output or reference it from tracked files; screenshots stay in the run folder's `screens/`, findings in the run folder's `findings.md`.

## Concrete input example (hospital-helpdesk, RHOAI 3.5) — illustrative only, replace values
```
- Tutorial: workshop/docs (Antora site; npm run dev, review rendered pages at :3000)
- Platform: Red Hat OpenShift AI 3.5 dashboard; creds: user1 lines in .creds
- Findings file: `review/2026-09-21-hospital-helpdesk/findings.md`
- Review folder: `review/2026-09-21-hospital-helpdesk/` (git-ignored run folder) — screenshots: `review/2026-09-21-hospital-helpdesk/screens/<module>-<step>-<short-name>.png`
- Known-good: RHOAI 3.5 DSC Ready, genAiStudio enabled, model registry Ready, gen-ai-aa-mcp-servers ConfigMap present, S3 model storage ready, MCP ticketing server reachable
```

