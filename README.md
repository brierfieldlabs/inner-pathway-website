# Inner Pathway Counselling website

Authoritative source repository for the Inner Pathway Counselling website.

## Published websites and repositories

| Purpose | Source | Published address |
| --- | --- | --- |
| Approved live website | `brierfieldlabs/inner-pathway-website` branch `main` | https://innerpathway.co.uk/ |
| Public review website | `brierfieldlabs/inner-pathway-website` branch `staging` | https://staging.innerpathway.co.uk/ |

**All website editing takes place in this source repository.** The public review site is automatically copied into the separate **generated** repository `brierfieldlabs/inner-pathway-staging`. Do **not** edit that generated repository manually or grant normal website contributors write access to it. Debi (`deupton-ip`) needs write access to this source repository only.

The public staging site contains a draft banner and blocks indexing (`noindex,nofollow` and `robots.txt`). The live site remains indexable. The production domain uses GitHub Pages and IONOS DNS; never change the domain or mail-related DNS as part of ordinary website editing.

## Development and approval

Read [AGENTS.md](AGENTS.md) for the **authoritative edit, preview, approval, publication and rollback workflow**.

- Normal updates are submitted through a short-lived branch and PR to **`staging`**, with validation before merging.
- After source `staging` changes, Hamblett **CT140** runs `inner-pathway-preview-sync.timer` every 10 minutes. `/usr/local/sbin/inner-pathway-preview-sync` builds and pushes the preview into `brierfieldlabs/inner-pathway-staging`; that repository's GitHub Pages publishes the public staging URL.
- Verify publication by comparing the source branch commit with the generated repository's `README.md` **Source commit**, checking its GitHub Pages deployment and inspecting the public staging URL.
- The separate isolated **CT146 local preview** is not the public GitHub Pages staging website.
- Only explicit approval from Debi or Darren permits a **scoped** publication PR into `main`. Unapproved staging changes must remain out of production.
- The source `.github/workflows/pages.yml` validates both source branches, but deploys **production only from `main`** after validation. A push to `staging` does not deploy production.

Development Git work is carried out on Hamblett CT140, with GitHub Actions using Hamblett self-hosted runners, not Darren's laptop.

Local validation:

```bash
python3 scripts/validate-site.py
```

## Website content and safeguards

The website is based on approved Inner Pathway counselling information, professional information, the established logo and branding, and relevant admin/legal material. No private client or clinical data belongs in the repository.

The legacy IONOS `/references/` page was intentionally omitted because it contained generic template wording and placeholder contact details. The new site retains useful themes around counselling, Debi's experience, adult clients, carers, neurodivergence, face-to-face/online/telephone work and resources, while omitting the old contact form, translation widget and marketing-tracker consent layer.
