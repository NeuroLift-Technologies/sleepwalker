# SOP: Incident Response — Agent Goes Off-Rails

**SOP ID:** SOP-NLT-003  
**Version:** 1.0.0  
**Scope:** Responding to a coding agent that has deviated from governance protocols  
**Authority:** Joshua W. Dorsey, Sr.  
**Governed by:** ORG-DEV-OTOI-1.0.2

---

## Purpose

This SOP defines the response procedure when a coding agent has:
- Made unauthorized architectural decisions
- Committed sensitive data (credentials, secrets)
- Gone beyond authorized scope
- Taken irreversible actions without approval
- Behaved in ways inconsistent with ORG-DEV-OTOI-1.0.2

---

## Severity Classification

| Severity | Examples |
|---|---|
| **Critical** | Secrets committed, production systems modified, external systems accessed without approval |
| **High** | Unauthorized architecture decisions, scope significantly exceeded, data integrity affected |
| **Medium** | Commit format violations, missing handoff records, active-threads.md not updated |
| **Low** | Minor protocol deviations with no functional impact |

---

## Immediate Response (Critical / High)

### Step 1: Stop the Agent

Terminate the agent session immediately. Do not allow further commits.

If using GitHub Copilot / Codex CLI / Claude Code / similar: end the session.

### Step 2: Assess the Damage

Answer these questions:
1. What unauthorized actions were taken?
2. Are secrets or credentials exposed? → If yes, treat as security incident immediately
3. Were production systems affected?
4. What is the current state of the working branch/repo?
5. Is any data at risk?

### Step 3: Secure (if credentials exposed)

If any secrets, tokens, API keys, or credentials were committed:

1. **Immediately revoke** all exposed credentials — treat as compromised
2. Rotate all secrets referenced in or near the affected commits
3. Remove secrets from git history (use `git filter-branch` or BFG Repo Cleaner)
4. Force-push the cleaned branch
5. Audit all systems that used the exposed credentials

**This must happen within minutes, not hours.**

### Step 4: Revert Unauthorized Changes

For unauthorized code or configuration changes:

```bash
# Option A: Revert specific commits
git revert [commit-sha]

# Option B: Reset branch to last known-good state
git reset --hard [last-good-sha]
git push --force-with-lease origin [branch]
```

Document what was reverted and why.

### Step 5: Document the Incident

Create an incident record at `docs/escalations/incident-[date]-[brief-description].md`:

```markdown
## Incident Record

**Date:** [ISO 8601]
**Severity:** [Critical | High | Medium | Low]
**Agent involved:** [Agent name / platform]
**Session:** [Branch or session ID]
**Reported by:** [Name]

### What Happened
[Factual description of what the agent did]

### Impact
[What systems, data, or processes were affected]

### Actions Taken
1. [Action with timestamp]
2. [Action with timestamp]

### Root Cause
[Why did the agent deviate? Unclear instructions? Missing guardrail? OTOI gap?]

### Prevention
[What changes will prevent recurrence?]
```

---

## Standard Response (Medium / Low)

### Step 1: Document the Deviation

Add to `docs/escalations/` with severity and description.

### Step 2: Correct the Work

Review all commits since the deviation and correct any improper work:
- Fix commit messages to follow format
- Add missing handoff records retroactively
- Update active-threads.md to reflect accurate state

### Step 3: Review with Joshua

Bring the deviation to Joshua's attention even for medium/low severity. He determines whether protocol amendments are needed.

---

## Post-Incident Review

After any incident, conduct a review:

1. **What happened?** — Timeline of events
2. **Why did it happen?** — Root cause (unclear instructions, missing guardrail, agent limitation)
3. **What was the impact?** — Systems, data, time, trust
4. **What changed?** — Reverted code, rotated credentials, cleaned history
5. **What prevents recurrence?** — OTOI amendment? Better CLAUDE.md? Clearer task scoping?

File a `governance-proposal` GitHub issue if OTOI amendments are needed.

---

## Escalation

All critical and high severity incidents must be escalated to Joshua W. Dorsey, Sr. immediately:

- File GitHub issue using `ISSUE_TEMPLATE/agent-escalation.md`
- Contact: info@neuroliftsolutions.com
- Priority: **critical**

---

## Prevention

The best incident response is prevention. Ensure every agent:
- Reads and acknowledges ORG-DEV-OTOI-1.0.2 before beginning
- Self-registers per OTOI Section 3
- Has clear, specific task scope confirmed before starting
- Knows to escalate rather than guess

See `SOPs/new-agent-onboarding.md` for the full onboarding checklist.

### Credential Exposure Controls

As of 2026-05-22, this repository includes the governance validation workflow
`.github/workflows/validate-governance.yml`, but it does **not** include credential
scanning workflows or local secret-scanning hook templates.

If a credential exposure occurs, do not assume automation has opened an incident or
blocked the merge. Follow the immediate response steps above, then manually verify:

1. The affected credential was revoked and rotated.
2. The exposed value was removed from the branch and, if needed, git history.
3. The incident record was written under `docs/escalations/`.
4. Joshua W. Dorsey, Sr. reviewed the incident and any required follow-up controls.

#### Future Automated Gates

If credential scanning workflows are added later, document the exact workflow files,
trigger conditions, and required status-check names here. Also add them to
`.nltotoi/index/governance-files.md` once the files exist.

#### GitHub Native Secret Scanning

Enable GitHub's built-in secret scanning for all NLT repositories:

- **Settings → Advanced Security → Secret scanning** — detects 200+ provider token formats
- Enable **"Push protection"** to block pushes containing known secret patterns at the server level
- Enable **"Scan for non-provider patterns"** for generic API keys and connection strings

---

*SOP-NLT-003 v1.0.0 | NeuroLift Technologies | ORG-DEV-OTOI-1.0.2*
