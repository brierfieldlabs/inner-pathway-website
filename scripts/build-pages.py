#!/usr/bin/env python3
"""Assemble live and staging copies into one GitHub Pages artifact."""
from __future__ import annotations
import argparse
import re
import shutil
from pathlib import Path

EXCLUDED_TOP_LEVEL = {
    ".git", ".github", "history", "scripts", "AGENTS.md", "README.md", ".gitignore"
}
ALLOWED_HIDDEN = {".nojekyll"}
ROBOTS_META = '<meta name="robots" content="noindex,nofollow">'
STAGING_BANNER = (
    '<div class="staging-banner" data-staging-banner role="status">'
    'TEST VERSION · Changes here are not live'
    '</div>'
)
STAGING_CSS = """

/* Added only to the deployed staging copy. */
.staging-banner {
  position: sticky;
  top: 0;
  z-index: 99999;
  box-sizing: border-box;
  width: 100%;
  padding: 9px 14px;
  background: #60233a;
  color: #fff;
  text-align: center;
  font: 700 clamp(.76rem, 2.8vw, .88rem)/1.25 system-ui, sans-serif;
  letter-spacing: .035em;
}
"""


def copy_public_site(source: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for item in source.iterdir():
        if item.name in EXCLUDED_TOP_LEVEL:
            continue
        if item.name.startswith(".") and item.name not in ALLOWED_HIDDEN:
            continue
        target = destination / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)


def protect_staging(staging_root: Path) -> None:
    robots_re = re.compile(
        r'<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*["\']\s*/?>',
        flags=re.IGNORECASE,
    )
    body_re = re.compile(r'(<body(?:\s[^>]*)?>)', flags=re.IGNORECASE)
    for html_path in staging_root.rglob("*.html"):
        text = html_path.read_text(encoding="utf-8")
        if robots_re.search(text):
            text = robots_re.sub(ROBOTS_META, text, count=1)
        else:
            text = re.sub(r"</head>", f"  {ROBOTS_META}\n</head>", text, count=1, flags=re.IGNORECASE)
        if "data-staging-banner" not in text:
            text = body_re.sub(rf"\1\n  {STAGING_BANNER}", text, count=1)
        html_path.write_text(text, encoding="utf-8")

    css_path = staging_root / "assets" / "site.css"
    if css_path.exists():
        css = css_path.read_text(encoding="utf-8")
        if "Added only to the deployed staging copy" not in css:
            css_path.write_text(css + STAGING_CSS, encoding="utf-8")

    # The test copy must never claim the production custom domain.
    cname = staging_root / "CNAME"
    if cname.exists():
        cname.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", required=True, type=Path)
    parser.add_argument("--staging", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    output = args.output.resolve()
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    copy_public_site(args.live.resolve(), output)
    staging_output = output / "staging"
    copy_public_site(args.staging.resolve(), staging_output)
    protect_staging(staging_output)

    if not (output / "index.html").exists():
        raise SystemExit("live index.html missing from Pages artifact")
    if not (staging_output / "index.html").exists():
        raise SystemExit("staging index.html missing from Pages artifact")
    print(f"Built live site at {output}")
    print(f"Built protected staging site at {staging_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
