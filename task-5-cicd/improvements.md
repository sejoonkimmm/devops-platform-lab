# Task 5: Improve the CI/CD pipeline

Rewritten pipeline: `azure-pipelines.yml` (+ `templates/setup-node.yml`), in this folder.

## What made it slow, and what I changed

The original ran five sequential stages, and every job did `checkout` + `npm install` from scratch. Azure DevOps gives each job a fresh agent, so that meant installing dependencies five times, one after another, with no caching.

| Change | Why it matters |
|---|---|
| `npm install` → `npm ci` | Installs from `package-lock.json`, skips resolution, and is meant for CI. Faster and reproducible. |
| Added `Cache@2` keyed on `package-lock.json` | Restores `node_modules`/npm cache between runs. The first run warms it, later runs skip most of the download. |
| Lint + unit tests in one stage as parallel jobs | They don't depend on each other. Running them side by side removes one full serial stage. |
| Pulled the repeated setup into `templates/setup-node.yml` | One place defines checkout + Node + cache + install. Every job uses it, so the install path is consistent instead of copy-pasted. |
| Pinned `ubuntu-24.04` (was `ubuntu-latest`) | `latest` changes under you and breaks builds silently. Pinning keeps builds reproducible. |
| `publish`/`download` artifact for build → deploy | Build output is passed to deploy instead of rebuilt. |

Net effect: dependencies install once per job with a warm cache, and lint/unit no longer wait in line.

## Most impactful, in order

1. **Dependency caching + `npm ci`.** This is the real fix for "the pipeline is slow." Repeated uncached installs were the bulk of the wall-clock time.
2. **Parallel lint and unit tests.** Removes an entire serial stage from the critical path.
3. **Pinned agent image.** Cheap change, saves the random red build that has nothing to do with your code.

## Issues beyond performance

These matter more than speed.

- **Hardcoded secrets in the YAML.** `DB_PASSWORD`, `API_KEY`, and `NPM_TOKEN` are committed in plain text. Two problems, not one:
  1. They must move out of the file into a secret variable group backed by Key Vault (done in the rewrite via `- group: app-secrets`).
  2. **They are already leaked.** Anything committed to git is in the history and must be treated as compromised. Moving them is not enough. All three have to be rotated, and cleaned out of the git history. This is the first thing I'd do, before touching performance.
- **`continueOnError: true` on lint.** Lint failures were being swallowed, so the "passing" pipeline could still merge code that violates the lint rules. Removed, so lint can fail the build again.
- **Deploy runs on every push to `main` with no gate.** No approval, no environment, no rollback path. One bad merge goes straight to production. The rewrite deploys through an `environment: production`, which adds a manual approval, deployment history, and a rollback target.
- **No verification after deploy.** The release step fires a `curl` and assumes success. Added `set -euo pipefail` and `curl -sf` so a failed release actually fails the job, but a real setup should also run a smoke test and be able to roll back.
- **No dependency/security scan.** Worth adding `npm audit` (or a proper SCA step) as a non-blocking stage to start, blocking later.
