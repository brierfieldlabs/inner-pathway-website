# Inner Pathway Counselling website

Static replacement website for Inner Pathway Counselling.

## Status

Preview v0.1.0. The repository is public so GitHub Pages can host the preview, but the site is intentionally marked `noindex,nofollow` and `robots.txt` blocks indexing until explicit launch approval.

The live `innerpathway.co.uk` domain is **not** changed by this repository.

## Development

Development Git work is carried out on Hamblett CT140. CI must run on the Hamblett self-hosted GitHub Actions runner, not on Darren's laptop.

Validation:

```bash
python3 scripts/validate-site.py
```

## Deployment

GitHub Pages deployment is performed by `.github/workflows/pages.yml` after validation passes on `main`.

Before launch:

1. Debi/Darren approve copy and design.
2. Remove `noindex,nofollow` and change `robots.txt` to allow indexing.
3. Add the approved custom domain with `CNAME`.
4. Change DNS only after the GitHub Pages custom-domain check is healthy.
5. Keep the previous hosting arrangement available until the cutover is verified.

## Source material

The draft is based on the current Inner Pathway website, the existing Inner Pathway admin/legal material, the established Inner Pathway logo, and confirmed current professional information. No Clinical data belongs in this repository.
