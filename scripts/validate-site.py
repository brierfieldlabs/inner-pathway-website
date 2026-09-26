#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import sys

ROOT = Path(__file__).resolve().parents[1]
HTML = [ROOT / "index.html", ROOT / "privacy.html", ROOT / "legal.html", ROOT / "404.html"]
REQUIRED = [
    ROOT / "assets/site.css",
    ROOT / "assets/site.js",
    ROOT / "assets/inner-pathway-logo.png",
    ROOT / "assets/online-telephone-counselling-badge.png",
    ROOT / "assets/photos/debi-portrait.png",
    ROOT / "assets/photos/debi-portrait-920.webp",
    ROOT / "assets/photos/debi-counselling-room.jpg",
    ROOT / "assets/resources/float-framework.png",
    ROOT / "assets/resources/inner-pathway-reflective-journal.png",
    ROOT / "robots.txt",
    ROOT / ".nojekyll",
]

errors = []

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []
        self.title = []
        self.in_title = False
        self.meta_robots = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"): self.links.append(a["href"])
        if tag == "img" and a.get("src"): self.images.append(a["src"])
        if tag == "title": self.in_title = True
        if tag == "meta" and a.get("name","").lower() == "robots":
            self.meta_robots.append(a.get("content",""))
    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
    def handle_data(self, data):
        if self.in_title: self.title.append(data)

for path in HTML + REQUIRED:
    if not path.exists():
        errors.append(f"missing required file: {path.relative_to(ROOT)}")

for path in HTML:
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    parser = Parser()
    parser.feed(text)
    if not "".join(parser.title).strip():
        errors.append(f"{path.name}: missing title")
    if '<meta name="viewport" content="width=device-width, initial-scale=1">' not in text:
        errors.append(f"{path.name}: missing responsive viewport metadata")
    if path.name != "404.html":
        robots = " ".join(parser.meta_robots).lower()
        if "noindex" not in robots:
            errors.append(f"{path.name}: preview must remain noindex until launch approval")
    for target in parser.links + parser.images:
        parsed = urlparse(target)
        if parsed.scheme in {"http","https","mailto","tel"} or target.startswith("#"):
            continue
        local = (path.parent / parsed.path).resolve()
        try:
            local.relative_to(ROOT)
        except ValueError:
            errors.append(f"{path.name}: path escapes repository: {target}")
            continue
        if not local.exists():
            errors.append(f"{path.name}: broken local reference: {target}")

index = (ROOT / "index.html").read_text(encoding="utf-8")
for needle in [
    "Inner Pathway Counselling",
    "Certificate in Online and Telephone Counselling",
    "A Therapeutic Focus on Risk When Working with Sexual Harm and its Consequences",
    "BACP Individual Member",
    "The F.L.O.A.T Framework",
    "The Inner Pathway Reflective Journal",
    "£50",
    "A limited number of reduced-fee spaces are available.",
    "debi@innerpathway.co.uk",
]:
    if needle not in index:
        errors.append(f"index.html: missing required content: {needle}")

robots = (ROOT / "robots.txt").read_text(encoding="utf-8") if (ROOT / "robots.txt").exists() else ""
if "Disallow: /" not in robots:
    errors.append("robots.txt must block indexing during preview")

for banned in ["TODO", "Lorem ipsum", "example.com"]:
    for path in HTML:
        if path.exists() and banned.lower() in path.read_text(encoding="utf-8").lower():
            errors.append(f"{path.name}: placeholder content found: {banned}")

if errors:
    print("Website validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)

print("Website validation passed.")
