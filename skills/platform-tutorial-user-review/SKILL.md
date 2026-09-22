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

## Tooling
- Drive the platform UI with a browser-automation tool — Playwright (headless is fine; pin the browser revision and pass `executable_path` when the install is managed) or an equivalent harness (browser tab helpers, aria snapshots, screenshots). Every verification is from the UI point of view.
- Screenshot plumbing gotcha: the harness may save captures to a temp dir (webp) instead of the requested path. Locate the newest temp captures, visually verify each file's content before mapping it to a step name (never trust capture order alone), convert to PNG into the run folder's `screens/`, and reference those paths in findings.
- `oc`/`kubectl` are frowned upon for regular RHOAI users — not part of the learner's toolchain. Run them only when the tutorial itself instructs a CLI step, and record that dependency in the findings.

## Run in sub-agents (keep the orchestrating context clean)
- Do the walkthrough in background sub-agents, not inline: the main session only orchestrates. One sub-agent per module (or a small range of modules), run in order — later modules depend on earlier state.
- Each sub-agent's brief: its module range, this skill (point it at the skill file so it reads the full rules), and the shared inputs (tutorial location, UI URL, creds path, review folder). Sub-agents start blank — everything they need must be in the brief.
- Sub-agents write straight to the review folder: findings appended to `findings.md`, screenshots to `screens/`, logs and HTML dumps to files. They return only a short summary: modules completed/failed, findings count, screenshot paths, open questions for the admin.
- Never paste full page HTML, aria snapshots, or long CLI output back into the orchestrating conversation — those are files in the run folder, referenced by path.
- Orchestrator platform health: verify the platform UI is reachable before dispatching each module (and after long waits). An outage silently poisons sub-agent findings — verify the cause (e.g. kubelet events), recover if trivial, and log the outage window + cause in the findings header as **platform state**, not tutorial findings.
- Orchestrator/admin interventions during the run (creating a hardware profile, deleting a crash-looping resource, enabling a flag) go in the findings header as logged admin actions — never reported as sub-agent successes.
- Tooling churn cap: if a sub-agent rewrites its automation driver more than ~3 times for one step, steer it to stop, record a tooling-bounded finding (see Capture per step), append its module section, and return. A completed module with an honest "not verified" note beats another hour of driver churn.

## Work through every module in order, as a learner would
- Alternatives (scripted vs manual, UI vs CLI, optional vs required): take the primary path first, note the alternative exists.
- Optional step: ask whether later modules depend on it — skip once, note downstream breakage, go back and complete if needed. "The docs don't say what this optional step feeds" is a finding either way.

## Capture per step
1. **Instruction vs UI**: where the doc's words differ from what you see (button labels, menus, step order, missing elements). Screenshot every mismatch: `<review-run>/screens/<module>-<step>-<short-name>.png`.
2. **Does it work?** Success/failure per step; on failure capture exact error text (screenshot + copy). Classify it: doc-vs-UI mismatch → a finding; missing platform prerequisite the learner cannot fix (model never Ready, service absent, per-project feature not enabled) → an **untestable platform gap** (one line referencing the header's platform-state bullet — not a doc failure); automation limits (a step could not be executed/verified) → a **tooling-bounded** note stating exactly what was and was not executed.
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
- Make the "could a first-time user complete this alone?" answer explicit about the cluster state it holds for (hardware profiles, catalog generation, feature operators, per-project enablement) so docs authors can separate doc defects from platform provisioning.
- Group repeated blockers by root cause: when one missing prerequisite (e.g. a hardcoded service URL) fails steps across several modules, rank it once at the top instead of restating it per module.

## Expected state (from the admin)
`<paste the admin's handoff checklist here>`. A step failing in a way this list says was pre-configured → mismatch between handoff note and reality, not your error.
The findings header also carries **platform state**: orchestrator-verified outage causes + recovery, and admin interventions performed during the run. Sub-agent findings reference this header; a step failing the way this state predicts → platform gap, not a doc or user error.

## Rules
- Follow the tutorial **in order**; no skipping ahead. A step that only works via something the tutorial didn't say is a finding, not a success.
- Never edit the tutorial's source to make a step pass.
- No outside sources unless a step is truly impossible — then note it, try the most likely alternative, report what you had to do.
- Screenshot everything you'd show a colleague when explaining a problem.
- Be specific: exact button labels, exact error text, exact screenshots.
- Verify everything from the UI point of view with a browser-automation tool (see Tooling above). `oc`/`kubectl` are frowned upon for regular RHOAI users — use them only when the tutorial itself instructs it, and flag it as a finding.

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

