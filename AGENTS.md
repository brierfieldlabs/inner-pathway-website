# Inner Pathway website agent workflow

This repository is the Inner Pathway Counselling website. Debi and Darren both manage it through ChatGPT. **Normal edits go to staging, never directly to the live branch.**

## Branch roles

- `staging` is the editable/test website. All normal website changes requested by Debi or Darren go here first.
- `main` is the live website source. Never edit or push directly to `main`.
- GitHub Pages publishes both from this one repository: live at the site root and test at `/staging/`.
- The deployed staging copy is automatically marked `TEST SITE · Changes here are not live` and forced to `noindex,nofollow`.

## Normal edit workflow

When Debi or Darren asks to change, update, add, remove, redesign or fix something on the website, that means **staging only** unless they explicitly ask to publish/promote it.

1. Fetch the latest repository state and start from current `origin/staging`.
2. Create a short-lived change branch from `staging`. Never edit or push directly to `staging` or `main`.
3. Make only the requested change on that branch.
4. Preserve the Inner Pathway visual identity unless the user explicitly requests a redesign.
5. Keep every change mobile-friendly. When browser tooling is available, run `python3 scripts/check-responsive.py --root . --screenshots /tmp/inner-pathway-responsive` to test approximately 320, 390, 768 and 1440 px widths, including overflow and touch targets.
6. Run `python3 scripts/validate-site.py`.
7. Commit and push the change branch using the connected user's GitHub identity.
8. Open a pull request from the change branch into `staging`. No human approval is required.
9. Wait for the required `Validate static site` check. Fix failures on the change branch.
10. When green, squash-merge the PR into `staging` and delete the temporary branch.
11. Wait for the staging GitHub Pages deployment to succeed.
12. Confirm the deployed staging page loads and give the user the staging URL for review.
13. Do **not** promote the change to `main` merely because staging CI is green.

Each staging PR should represent one coherent requested change where practical. This makes changes independently reversible.

## Publishing a tested change

Only publish when Debi or Darren explicitly says the staging site is approved and asks to publish, promote, make live, or equivalent.

1. Confirm `staging` is clean, pushed, deployed, and its latest validation is green.
2. Compare `staging` with `main` and summarise what will go live.
3. Open a pull request from `staging` to `main`.
4. Wait for the required `Validate static site` check.
5. If it fails, fix the problem on `staging`, redeploy staging, and re-check before proceeding.
6. When green, merge the PR. No separate human GitHub reviewer is required because the user already gave the publish instruction in ChatGPT.
7. Bring `staging` forward to the resulting `main` commit and push it so both branches are aligned after release.
8. Confirm the GitHub Pages live-root deployment succeeds and verify the requested change there.

## Reverting a staging change

If Debi or Darren asks to undo, revert or roll back a change that has already reached staging:

1. Identify the staging squash commit or pull request that introduced that specific change.
2. Create a new short-lived revert branch from current `staging`.
3. Use `git revert` on that commit rather than resetting or rewriting branch history.
4. Run validation and responsive QA as appropriate.
5. Push the revert branch and open a pull request into `staging`.
6. When `Validate static site` is green, squash-merge the revert PR.
7. Verify the staging deployment.

Never use `reset --hard`, force-push, or branch rewrites to undo shared staging history. Existing staging commits made before this PR-first rule are still reversible with `git revert` by commit SHA.

## Safety rails

- Never edit, commit to, or push directly to `main` or `staging`.
- Never interpret an ordinary website-edit request as permission to publish it live.
- Do not force-push or delete `main` or `staging`.
- Do not alter the production custom domain, live DNS, indexing policy, or launch safeguards unless the user explicitly requests that specific operation.
- Do not expose private client or clinical information anywhere in this public repository.
- Keep changes mobile-friendly and verify narrow layouts before presenting staging as ready.
- Do not use version numbers or version prefixes in commit messages, pull-request titles, branch names, tags, website copy or project documentation.
- Prefer concise, descriptive commit and pull-request titles.

## Deployment

GitHub Pages is assembled from both `main` and `staging` only after validation succeeds. The self-hosted CI runner is at Hamblett; contributors do not need access to Darren's laptop.
