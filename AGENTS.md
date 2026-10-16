# Inner Pathway website agent workflow

## Brierfield Labs engineering standard (ChatGPT/Codex)

Before any new coding task, check current GitHub issues/PRs and accepted project decisions rather than relying on conversation history. Apply the [Brierfield Labs Coding House Rules](https://github.com/brierfieldlabs/infrastructure/blob/main/procedures/coding-house-rules.md) (for authorised users), with the [public proportionate-engineering summary](https://github.com/brierfieldpathway/.github/blob/main/CONTRIBUTING.md) as accessible guidance.

**Agreed scope only.** Interesting ideas belong in deferred/proposed GitHub issues until explicitly accepted. Prefer the smallest maintainable implementation, existing tools, targeted tests and security that addresses real risks. Do not invent subsystems, encryption, extra CI or unapproved features. Respect previously agreed decisions and preserve all stricter repository-specific release, data-safety and approval requirements below. Push coherent work, reconcile GitHub issues/PRs and record one concrete next step.

This repository is the **authoritative source** for the Inner Pathway Counselling website. Debi and Darren manage website changes through ChatGPT. **Ordinary website edits go to the `staging` branch first, never straight to the live site.**

## Source branches and published sites

- `brierfieldlabs/inner-pathway-website` is the **only editable source repository**.
- `staging` is the source branch for testing and review.
- `main` is the approved production source for **https://innerpathway.co.uk/**.
- **https://staging.innerpathway.co.uk/** is published from the separate generated repository `brierfieldlabs/inner-pathway-staging` (`main`). **Do not edit this generated repository directly.**
- Hamblett CT140 runs `inner-pathway-preview-sync.timer` every 10 minutes. Its `/usr/local/sbin/inner-pathway-preview-sync` job validates the source `staging` branch, builds a non-indexable preview, and pushes it to the generated repository. GitHub Pages then publishes that repository.
- Hamblett CT146 also runs an isolated *local* preview. It is **not** the public GitHub Pages preview and does not replace the CT140 publishing process.
- The public preview has an obvious draft banner, `noindex,nofollow`, and a blocking `robots.txt`. It must never be used as the production Pages source.
- The source repository's `.github/workflows/pages.yml` validates changes on `main` and `staging`, but **only a successful push to `main` deploys production GitHub Pages**. Pushing to `staging` does not deploy production.

## Normal website change workflow

When Debi or Darren asks to update the website, interpret this as **staging only** unless they explicitly ask to publish an approved change.

1. Read this file and fetch the latest state of `brierfieldlabs/inner-pathway-website`, especially `origin/staging`.
2. Create a short-lived branch **from the current `staging`**; never commit directly to `staging` or `main`.
3. Make only the requested edit. Preserve the established visual identity unless asked to redesign.
4. Keep pages mobile-friendly. When browser tooling is available, run `python3 scripts/check-responsive.py --root . --screenshots /tmp/inner-pathway-responsive` to check approximately 320, 390, 768 and 1440 px layouts.
5. Run `python3 scripts/validate-site.py`.
6. Commit and push the change branch using the connected user's GitHub identity, then open a PR **into the source repository's `staging` branch**.
7. Wait for the required `Validate static site` check; fix any failures. When green, squash-merge the PR into `staging` and delete the temporary branch.
8. Allow the CT140 synchronisation cycle (up to 10 minutes) and GitHub Pages deployment to complete. Verify the generated repository's `README.md` **Source commit** matches the source `staging` commit; confirm its Pages deployment succeeded.
9. Verify the requested change at **https://staging.innerpathway.co.uk/** and give Debi or Darren that link for review. Account for browser caching if GitHub Pages has deployed.
10. **Do not publish to `main` merely because staging CI or the preview succeeded.**

The generated preview repository is intentionally **read-only for normal website editors**, including Debi. The CT140 synchronisation job has the required publication access. **Never ask to grant `deupton-ip` write access to `inner-pathway-staging` to complete an ordinary edit.** If the preview is stale, diagnose the source `staging` commit, CT140 timer/service, generated repository's source commit and GitHub Pages deployment in that order.

Each staging PR should represent one coherent requested change where practical, to make changes independently reversible.

## Publishing an approved change

Only publish if Debi or Darren **explicitly approves the tested change and asks for it to go live**.

1. Confirm the requested change is visible on the public staging URL and the validation and preview deployment succeeded.
2. Compare `staging` with `main`; describe **exactly** which changes would reach production. Never bundle other unapproved staging work.
3. If every difference is explicitly approved, a PR from `staging` to `main` is appropriate. If staging contains other work, instead create a release branch from `main` containing **only** the approved changes and open its PR into `main`.
4. Wait for `Validate static site`; fix failures on the proposed branch, revalidate and re-review any changed public copy as necessary.
5. Merge only the approved PR. No separate GitHub reviewer is required after the user has expressly approved publication in ChatGPT.
6. Confirm the source repository's production GitHub Pages deployment succeeded and verify the approved change at **https://innerpathway.co.uk/**.
7. Reconcile any divergent `staging` history using a reviewed PR, rather than force-pushing or silently resetting it.

## Reverting staging

For a rollback, identify the staging PR/squash commit, branch from the current source `staging`, revert that change without rewriting history, validate, open a PR into `staging`, and merge once green. Verify the public staging deployment after the CT140 synchronisation and GitHub Pages finish. Never use `reset --hard` or force-push on shared branches.

## Safety rails

- Never commit or push directly to `main` or `staging`; use PRs.
- Never edit the generated `inner-pathway-staging` repository as a website source.
- Never treat a normal website edit as permission to publish live.
- Never force-push, reset, or delete either source branch.
- Do not change production DNS, custom domains, indexing, mail records, or launch safeguards without explicit instruction.
- Never publish private client or clinical information in these public repositories.
- Prefer concise descriptive commit messages, branches and PR titles; no version-number prefixes.
- All CI runs on the Hamblett self-hosted GitHub Actions runner. Contributors do not need access to Darren's laptop.
