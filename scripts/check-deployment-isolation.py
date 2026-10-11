#!/usr/bin/env python3
"""Fail closed if GitHub Pages could deploy staging as production."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
workflow = (root / ".github/workflows/pages.yml").read_text(encoding="utf-8")
builder = (root / "scripts/build-pages.py").read_text(encoding="utf-8")
expected = "if: github.event_name == 'push' && github.ref == 'refs/heads/main'"

assert workflow.count(expected) == 1, "Pages deploy must require push to main only"
assert "source-staging" not in workflow, "Production workflow must not checkout staging"
assert "--staging" not in workflow, "Production build must not accept a staging source"
assert 'if (output / "staging").exists():' in builder, "Builder must reject staged content"
assert '"staging"' in builder, "Builder must exclude staging directory"
assert "Deploy production-only GitHub Pages" in workflow
print("PASS: staging events cannot publish GitHub Pages; production build excludes staging")
