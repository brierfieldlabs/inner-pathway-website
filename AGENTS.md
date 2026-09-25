# Inner Pathway website agent workflow

This repository is the Inner Pathway Counselling website. Debi and Darren both manage it through ChatGPT. **Normal edits go to staging, never directly to the live branch.**

## Branch roles

- `staging` is the editable/test website. All normal website changes requested by Debi or Darren go here first.
- `main` is the live website source. Never edit or push directly to `main`.
- GitHub Pages publishes both from this one repository: live at the site root and test at `/staging/`.
- The deployed staging copy is automatically marked `TEST VERSION · Changes here are not live` and forced to `noindex,nofollow`.

## Normal edit workflow

When Debi or Darren asks to change, update, add, remove, redesign or fix something on the website, that means **staging only** unless they explicitly ask to publish/promote it.

1. Switch to `staging` and pull the latest `origin/staging`.
2. Make the requested change on `staging`.
3. Preserve the Inner Pathway visual identity unless the user explicitly requests a redesign.
4. Keep every change mobile-friendly. When browser tooling is available, run `python3 scripts/check-responsive.py --root . --screenshots /tmp/inner-pathway-responsive` to test approximately 320, 390, 768 and 1440 px widths, including overflow and touch targets.
5. Run `python3 scripts/validate-site.py`.
6. Commit and push to `staging` using the connected user's GitHub identity.
7. Wait for `Validate static site` and the GitHub Pages deployment to succeed.
8. Confirm the deployed staging page loads and give the user the staging URL for review.
9. Do **not** merge or promote the change to `main` merely because CI is green.

## Publishing a tested change

Only publish when Debi or Darren explicitly says the staging version is approved and asks to publish, promote, make live, or equivalent.

1. Confirm `staging` is clean, pushed, deployed, and its latest validation is green.
2. Compare `staging` with `main` and summarise what will go live.
3. Open a pull request from `staging` to `main`.
4. Wait for the required `Validate static site` check.
5. If it fails, fix the problem on `staging`, redeploy staging, and re-check before proceeding.
6. When green, merge the PR. No separate human GitHub reviewer is required because the user already gave the publish instruction in ChatGPT.
7. Bring `staging` forward to the resulting `main` commit and push it so both branches are aligned after release.
8. Create the semantic version tag for the published version when appropriate.
9. Confirm the GitHub Pages live-root deployment succeeds and verify the requested change there.

## Safety rails

- Never edit, commit to, or push directly to `main`.
- Never interpret an ordinary website-edit request as permission to publish it live.
- Do not force-push or delete `main` or `staging`.
- Do not alter the production custom domain, live DNS, indexing policy, or launch safeguards unless the user explicitly requests that specific operation.
- Do not expose private client or clinical information anywhere in this public repository.
- Keep changes mobile-friendly and verify narrow layouts before presenting staging as ready.
- Use semantic versions in the form `vX.Y.Z`; do not use a `web-` prefix.
- Prefer concise, descriptive commit and pull-request titles.

## Deployment

GitHub Pages is assembled from both `main` and `staging` only after validation succeeds. The self-hosted CI runner is at Hamblett; contributors do not need access to Darren's laptop.
