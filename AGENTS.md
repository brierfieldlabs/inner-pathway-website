# Inner Pathway website agent workflow

This repository is the Inner Pathway Counselling website.

## Required change workflow

For every website change requested by Debi or Darren:

1. Start from the current main branch.
2. Create a new branch. Never push a website change directly to main.
3. Make the requested change and keep the site responsive/mobile-friendly.
4. Preserve the existing Inner Pathway visual identity unless the user explicitly asks for a redesign.
5. Run python3 scripts/validate-site.py when a shell is available.
6. Push the branch and open a pull request to main.
7. Wait for the GitHub Actions check named Validate static site.
8. If the check fails, diagnose and fix it on the same branch.
9. When the required check is green, merge the pull request using squash merge. No separate human reviewer is required.
10. Confirm the GitHub Pages deployment succeeds after merge.

## Safety rails

- Do not bypass GitHub or the pull-request/CI workflow.
- Do not force-push or delete main.
- Do not remove noindex,nofollow, change robots.txt to permit indexing, configure the custom domain, or alter live DNS unless the user explicitly asks for the approved launch/cutover.
- Do not expose private client or clinical information anywhere in this public repository.
- Keep changes mobile-friendly. Check narrow layouts and avoid horizontal overflow.
- Use semantic versions in the form vX.Y.Z; do not use a web- prefix.
- Prefer concise, descriptive commit and pull-request titles.

## Deployment

GitHub Pages deploys from main only after the validation job succeeds. The self-hosted GitHub Actions runner is at Hamblett; contributors do not need access to Darren's laptop.
