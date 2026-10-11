#!/usr/bin/env python3
"""Create the production-only GitHub Pages artifact.

The /staging tree must never be included in a production Pages deployment.
Staging is published independently from the staging branch by CT146 at Hamblett.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

EXCLUDED_TOP_LEVEL = {
    ".git", ".github", "history", "scripts", "AGENTS.md", "README.md",
    ".gitignore", "staging"
}
ALLOWED_HIDDEN = {".nojekyll"}


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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    source = args.live.resolve()
    output = args.output.resolve()
    if output == source or output.is_relative_to(source):
        raise SystemExit("Refusing to build inside the live source tree")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    copy_public_site(source, output)
    if not (output / "index.html").is_file():
        raise SystemExit("Production index.html missing from Pages artifact")
    if (output / "staging").exists():
        raise SystemExit("SECURITY: staging material found in production artifact")
    for path in output.rglob("*.html"):
        if 'data-staging-banner' in path.read_text(encoding="utf-8"):
            raise SystemExit(f"SECURITY: staging banner in production page: {path}")
    print(f"Built production-only site at {output} (no /staging content)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
