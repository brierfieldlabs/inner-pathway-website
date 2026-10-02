# Inner Pathway website handover — 25 September 2026 afternoon

## Authoritative continuation point

Repository: `brierfieldlabs/inner-pathway-website`

Development workstation: Hamblett CT140 only. Do not use Darren's laptop for Git work.

Current production branch state before this handover:
- branch: `main`
- HEAD: `432a00f56ad008fb4465f3e1c4422ed6840bfdec`
- tag: `web-v0.2.0`
- working tree: clean

Current GitHub Pages preview:
- `https://brierfieldlabs.github.io/inner-pathway-website/`
- GitHub Pages build type: workflow
- HTTPS enforced
- no custom domain configured
- the live `innerpathway.co.uk` DNS has **not** been changed

The preview remains deliberately hidden from search indexing:
- pages use `noindex,nofollow`
- `robots.txt` contains `Disallow: /`

Do not remove those protections or change DNS without explicit Darren/Debi approval.

## Current release history

- `web-v0.1.0` — initial static site and Hamblett Pages CI
- `web-v0.1.1` — GitHub Pages actions updated to Node 24
- `web-v0.2.0` — current-site content parity and current professional information

Current merged PRs:
- PR #1 — `web-v0.1.1: update Pages actions to Node 24`
- PR #2 — `web-v0.2.0: bring replacement site to content parity`

Open website issue:
- #3 — **Prepare Inner Pathway website for launch**

## CI / runner

The website has its own Hamblett self-hosted GitHub Actions runner:

`github-runner-hamblett-01-inner-pathway-website`

Labels:
- `self-hosted`
- `Linux`
- `X64`
- `hamblett`
- `normal-ci`
- `github`

Runner status at handover: online and idle.

Workflow:
`.github/workflows/pages.yml`

Both validation and Pages deployment must use the Hamblett self-hosted runner. Do not move CI to Darren's laptop or to a Brierfield runner.

Latest successful main workflow:
- run `36126801618`
- HEAD `432a00f56ad008fb4465f3e1c4422ed6840bfdec`

## Current site files

- `index.html`
- `privacy.html`
- `legal.html`
- `404.html`
- `assets/site.css`
- `assets/site.js`
- `assets/inner-pathway-logo.png`
- `assets/online-telephone-counselling-badge.png`
- `scripts/validate-site.py`
- `.github/workflows/pages.yml`
- `robots.txt`
- `.nojekyll`

The actual established Inner Pathway logo is used. Do not redesign or substitute it.

## Content already migrated

The replacement site currently carries forward:
- counselling/about material from the existing Inner Pathway site;
- adults, carers/parent carers and neurodivergent-adult sections;
- face-to-face, online and telephone counselling;
- current contact details and office address;
- £50 standard 50-minute session price;
- £25 reduced carer rate, pending final public eligibility wording;
- Debi's BACP Individual Membership information;
- qualification/training list;
- Debi's newly completed **Certificate in Online and Telephone Counselling**;
- the Online & Telephone Counselling Certified Counsellor badge;
- current resource themes for the F.L.O.A.T Framework and Inner Pathway Reflective Journal;
- rewritten privacy/legal pages suitable for the static GitHub Pages arrangement;
- urgent-help signposting.

The old IONOS `/references/` page was intentionally not migrated because it contains generic template/portfolio wording and placeholder contact information rather than useful Inner Pathway content.

The old IONOS contact form, translation widget and marketing-tracker consent layer are also intentionally absent.

## Immediate outstanding request: Debi's photographs

Darren's latest request was:

> "Can we have Debi's pictures on there as well from the website"

This has **not yet been implemented** and should be the first continuation task.

The current live homepage contains several image assets. The primary current-site image URLs detected during the handover are:

- `https://www.innerpathway.co.uk/wp-content/uploads/go-x/u/9efae605-5b6e-404b-a262-ed878cc39c1e/l0,t110,w1149,h1149/image.png`
- `https://www.innerpathway.co.uk/wp-content/uploads/go-x/u/ba713905-8ece-4967-b7ba-d4d9de9cf193/l0,t0,w1810,h2000/image-1366x1509.jpg`
- `https://www.innerpathway.co.uk/wp-content/uploads/go-x/u/0084c42d-2b12-416e-bf46-60f5a254f323/image-384x577.png`
- `https://www.innerpathway.co.uk/wp-content/uploads/go-x/u/64408db5-8770-4368-ab8d-bd7ee328c5e3/image-384x544.png`

There are also multiple responsive derivatives of those files in the current site's HTML.

Before committing photos:
1. visually inspect the source images and identify which are actually Debi;
2. prefer the largest/original useful source rather than a small responsive derivative;
3. preserve source bytes where practical;
4. place them under a sensible folder such as `assets/photos/`;
5. use meaningful lowercase-hyphenated filenames;
6. add useful, non-intrusive alt text;
7. optimise layout/responsiveness, but do not alter Debi's appearance;
8. keep the site visually consistent with the established Inner Pathway branding.

A photo-led `web-v0.3.0` is the natural next semantic version if the change materially updates the site's visual presentation.

## Current design direction

The replacement is a responsive static site using:
- warm off-white/rose surfaces;
- established burgundy Inner Pathway colour family;
- the real Inner Pathway logo;
- serif display headings with clean sans-serif body text;
- compact cards and straightforward navigation;
- mobile menu in `assets/site.js`;
- no unnecessary framework or Node runtime requirement for the actual site.

It should feel like a modern extension of Inner Pathway, not a generic wellness template.

## Launch issue #3 still needs confirmation

Before final launch:
- destination/link for the F.L.O.A.T Framework;
- destination/link for the Inner Pathway Reflective Journal;
- final public wording for the £25 reduced carer rate / eligibility;
- Debi/Darren approval of copy and design;
- approval of the added photographs.

After approval only:
- configure the approved custom domain/CNAME;
- preserve Proton Mail MX/TXT records;
- change only web-hosting DNS records required for GitHub Pages;
- verify GitHub custom-domain health and HTTPS;
- remove `noindex,nofollow` and unblock `robots.txt`;
- verify desktop and mobile after DNS cutover;
- retire the old hosted website only after the new site is proven.

## Git / release conventions

Continue the established Brierfield-style website conventions:
- semantic web versions such as `web-v0.3.0`;
- Git tags in the same form;
- commit/PR titles beginning with the full version, e.g.
  `web-v0.3.0: add Debi photography and refine responsive layout (#N)`;
- work on a feature branch;
- PR through Hamblett CI;
- merge only when green;
- tag the merged release;
- do not bypass CI.

## Practice Manager separation

This website repository is separate from `brierfieldlabs/practice-manager`.

Do not use this work as a reason to alter the Practice Manager desktop evaluation lane. Debi's Practice Manager evaluation must remain independently responsive to feedback.

No Clinical data belongs in this website repository.

## Recommended next steps

1. Return to `main` after this handover PR is recorded.
2. Create a fresh `web/v0.3.0-...` feature branch.
3. Download and visually identify Debi's current-site photographs.
4. Add the selected photographs to the new site and refine desktop/mobile layout around them.
5. Run `python3 scripts/validate-site.py` only through the normal Git/CI workflow, with CI on Hamblett.
6. Open a PR with the full `web-v0.3.0` prefix.
7. Keep the preview noindex and leave live DNS untouched.
8. Show Darren the resulting Pages preview for approval.
