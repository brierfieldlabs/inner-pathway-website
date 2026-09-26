#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
HTML = [ROOT / "index.html", ROOT / "privacy.html", ROOT / "legal.html", ROOT / "404.html"]
REQUIRED = [
    ROOT / "assets/site.css",
    ROOT / "assets/site.js",
    ROOT / "assets/inner-pathway-logo.png",
    ROOT / "assets/inner-pathway-logo-256.webp",
    ROOT / "assets/online-telephone-counselling-badge.png",
    ROOT / "assets/photos/debi-portrait.png",
    ROOT / "assets/photos/debi-portrait-920.webp",
    ROOT / "assets/photos/debi-counselling-room.jpg",
    ROOT / "assets/resources/float-framework.png",
    ROOT / "assets/resources/inner-pathway-reflective-journal.png",
    ROOT / "robots.txt",
    ROOT / "sitemap.xml",
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
        self.canonicals = []
        self.meta_names = {}
        self.meta_properties = {}
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"): self.links.append(a["href"])
        if tag == "img" and a.get("src"): self.images.append(a["src"])
        if tag == "title": self.in_title = True
        if tag == "meta" and a.get("name"):
            self.meta_names[a["name"].lower()] = a.get("content", "")
        if tag == "meta" and a.get("property"):
            self.meta_properties[a["property"].lower()] = a.get("content", "")
        if tag == "meta" and a.get("name","").lower() == "robots":
            self.meta_robots.append(a.get("content",""))
        if tag == "link" and a.get("rel", "").lower() == "canonical" and a.get("href"):
            self.canonicals.append(a["href"])
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
        if "noindex" in robots or "nofollow" in robots:
            errors.append(f"{path.name}: live source must allow indexing and following")
        if "index" not in robots or "follow" not in robots:
            errors.append(f"{path.name}: live source must explicitly use index,follow")
        expected_canonical = {
            "index.html": "https://innerpathway.co.uk/",
            "privacy.html": "https://innerpathway.co.uk/privacy.html",
            "legal.html": "https://innerpathway.co.uk/legal.html",
        }[path.name]
        if parser.canonicals != [expected_canonical]:
            errors.append(f"{path.name}: canonical URL must be {expected_canonical}")
        expected_title = "".join(parser.title).strip()
        expected_description = parser.meta_names.get("description", "")
        expected_social = {
            "og:type": "website",
            "og:locale": "en_GB",
            "og:site_name": "Inner Pathway Counselling",
            "og:title": expected_title,
            "og:description": expected_description,
            "og:url": expected_canonical,
            "og:image": "https://innerpathway.co.uk/assets/inner-pathway-logo.png",
            "og:image:alt": "Inner Pathway Counselling logo",
        }
        for key, value in expected_social.items():
            if parser.meta_properties.get(key) != value:
                errors.append(f"{path.name}: {key} metadata must be {value}")
        expected_named_social = {
            "twitter:card": "summary",
            "twitter:title": expected_title,
            "twitter:description": expected_description,
            "twitter:image": "https://innerpathway.co.uk/assets/inner-pathway-logo.png",
            "twitter:image:alt": "Inner Pathway Counselling logo",
        }
        for key, value in expected_named_social.items():
            if parser.meta_names.get(key) != value:
                errors.append(f"{path.name}: {key} metadata must be {value}")
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
structured_match = re.search(
    r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
    index,
    flags=re.DOTALL,
)
if not structured_match:
    errors.append("index.html: missing JSON-LD structured business data")
else:
    try:
        structured = json.loads(structured_match.group(1))
    except json.JSONDecodeError as exc:
        errors.append(f"index.html: invalid JSON-LD: {exc}")
    else:
        expected_structured = {
            "@context": "https://schema.org",
            "@type": "ProfessionalService",
            "name": "Inner Pathway Counselling",
            "url": "https://innerpathway.co.uk/",
            "telephone": "+44 7363 056570",
            "email": "debi@innerpathway.co.uk",
        }
        for key, value in expected_structured.items():
            if structured.get(key) != value:
                errors.append(f"index.html: JSON-LD {key} must be {value}")
        address = structured.get("address", {})
        if address.get("postalCode") != "WN8 6UR":
            errors.append("index.html: JSON-LD postal address must identify WN8 6UR")
        membership = structured.get("memberOf", {})
        if membership.get("identifier") != "01020412":
            errors.append("index.html: JSON-LD BACP membership identifier must remain 01020412")
        expected_social_identities = [
            "https://www.instagram.com/innerpathwaycounselling/",
            "https://www.facebook.com/people/Inner-Pathway-Counselling/61590994575444/",
        ]
        if structured.get("sameAs") != expected_social_identities:
            errors.append("index.html: JSON-LD social identities must use the stable Instagram and Facebook URLs")

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
if "Allow: /" not in robots or "Disallow: /" in robots:
    errors.append("robots.txt must allow indexing on the live site")
if "Sitemap: https://innerpathway.co.uk/sitemap.xml" not in robots:
    errors.append("robots.txt must advertise the production sitemap")

sitemap_path = ROOT / "sitemap.xml"
if sitemap_path.exists():
    try:
        tree = ET.parse(sitemap_path)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = {node.text for node in tree.findall("sm:url/sm:loc", ns)}
        expected_urls = {
            "https://innerpathway.co.uk/",
            "https://innerpathway.co.uk/privacy.html",
            "https://innerpathway.co.uk/legal.html",
        }
        if urls != expected_urls:
            errors.append("sitemap.xml must list exactly the public HTML pages")
    except ET.ParseError as exc:
        errors.append(f"sitemap.xml: invalid XML: {exc}")

for path in HTML:
    if path.exists() and '<img src="assets/inner-pathway-logo.png"' in path.read_text(encoding="utf-8"):
        errors.append(f"{path.name}: visible header logo must use the lightweight WebP derivative")

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
