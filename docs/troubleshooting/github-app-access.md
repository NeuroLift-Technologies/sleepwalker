# GitHub App Access to `sleepwalker`

Coding agents must be able to read the private governance files in
`NeuroLift-Technologies/sleepwalker` before starting work in downstream NLT
repositories. If an agent reports 404s for `NLT-DEV-OTOI.md` or `AGENTS.md`, check
GitHub App repository access before assuming the file is missing.

## Symptoms

- The agent can access the working repository but cannot open:
  - `https://github.com/NeuroLift-Technologies/sleepwalker/blob/main/NLT-DEV-OTOI.md`
  - `https://github.com/NeuroLift-Technologies/sleepwalker/blob/main/AGENTS.md`
- The repository's `CLAUDE.md` points to `sleepwalker`, but the agent falls back to the
  public mirror URLs.
- Governance onboarding stops before registration because the private contract is
  unavailable.

## Required Access

For GitHub Apps installed with **Selected repositories** access, add both:

1. The repository where the agent is doing work.
2. `NeuroLift-Technologies/sleepwalker`.

Without `sleepwalker` access, the agent may have project code access but still be unable
to read the canonical governance contract.

## Fix

1. Open organization app installations:
   `https://github.com/organizations/NeuroLift-Technologies/settings/installations`
2. Select the GitHub App used by the agent.
3. Click **Configure**.
4. Under **Repository access**, choose either:
   - **All repositories**, or
   - **Selected repositories** with `sleepwalker` and the working repository included.
5. Save the installation changes.
6. Restart or re-run the agent session so it reloads repository permissions.

## Fallback

If access cannot be granted immediately, downstream `CLAUDE.md` files should include
public mirror URLs for the governance documents:

- `https://github.com/NeuroLift-Technologies/.github/blob/main/governance/NLT-DEV-OTOI.md`
- `https://github.com/NeuroLift-Technologies/.github/blob/main/governance/AGENTS.md`

The private `sleepwalker` files remain the authoritative primary source when accessible.
