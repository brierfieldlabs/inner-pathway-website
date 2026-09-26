# Inner Pathway Counselling website

Static replacement website for Inner Pathway Counselling.

## Status

The approved website is published through GitHub Pages at `innerpathway.co.uk`. The live source allows search-engine indexing, while the generated `/staging/` copy is automatically forced to `noindex,nofollow` and a blocking `robots.txt`.

The production custom domain is managed through GitHub Pages and IONOS DNS. Mail-related DNS records are independent of this repository and must not be changed as part of website work.

## Development

Development Git work is carried out on Hamblett CT140. CI must run on the Hamblett self-hosted GitHub Actions runner, not on Darren's laptop.

Validation:

```bash
python3 scripts/validate-site.py
```

## Deployment

GitHub Pages deployment is performed by `.github/workflows/pages.yml` after validation passes on `main`.

Production safeguards:

1. Normal edits go to `staging` first and are reviewed there.
2. Promotion to `main` happens only after explicit approval.
3. The live site remains indexable; the generated staging copy remains blocked from indexing.
4. Custom-domain and DNS changes require explicit approval and must not disturb mail-related DNS records.

## Source material

The draft is based on the current Inner Pathway website, the existing Inner Pathway admin/legal material, the established Inner Pathway logo, and confirmed current professional information. No Clinical data belongs in this repository.

## Content migration notes

The current IONOS `/references/` page is intentionally not migrated because it contains generic template/portfolio wording and placeholder contact information rather than Inner Pathway material.

The new draft retains the useful current-site themes around counselling, Debi's background, adults, carers, neurodivergence, face-to-face/online/telephone work and resources, while removing the IONOS contact form, translation widget and marketing-tracker consent layer.
