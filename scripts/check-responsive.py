#!/usr/bin/env python3
"""Headless responsive smoke test for Inner Pathway website."""
from __future__ import annotations
import argparse
import contextlib
import http.server
import json
import os
import shutil
import socketserver
import threading
import time
from pathlib import Path

VIEWPORTS = [(320, 568), (390, 844), (768, 1024), (1440, 1000)]


def start_server(root: Path):
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *_args):
            pass
    handler = lambda *a, **kw: QuietHandler(*a, directory=str(root), **kw)
    server = socketserver.TCPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, f"http://127.0.0.1:{server.server_address[1]}/"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="Test an already-served URL")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Static site root when --url is omitted")
    parser.add_argument("--screenshots", type=Path, help="Optional screenshot output directory")
    args = parser.parse_args()

    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
    except ImportError as exc:
        raise SystemExit("Selenium is not installed on this workbench") from exc

    server = None
    url = args.url
    if not url:
        server, url = start_server(args.root.resolve())

    if args.screenshots:
        args.screenshots.mkdir(parents=True, exist_ok=True)

    failures = []
    options = Options()
    browser_binary = shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome")
    driver_binary = shutil.which("chromedriver")
    if browser_binary:
        options.binary_location = browser_binary
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--hide-scrollbars")

    try:
        service = Service(executable_path=driver_binary) if driver_binary else Service()
        driver = webdriver.Chrome(service=service, options=options)
        for width, height in VIEWPORTS:
            driver.set_window_size(width, height)
            driver.get(url)
            time.sleep(0.35)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(0.2)
            driver.execute_script("window.scrollTo(0, 0)")
            result = driver.execute_script("""
                const offenders = [...document.querySelectorAll('body *')]
                  .filter(el => {
                    const r = el.getBoundingClientRect();
                    return r.width > 0 && (r.right > window.innerWidth + 1 || r.left < -1);
                  })
                  .slice(0, 12)
                  .map(el => `${el.tagName.toLowerCase()}.${el.className}`);
                const toggle = document.querySelector('.nav-toggle');
                const tr = toggle ? toggle.getBoundingClientRect() : null;
                return {
                  innerWidth: window.innerWidth,
                  scrollWidth: document.documentElement.scrollWidth,
                  offenders,
                  brokenImages: [...document.images]
                    .filter(i => i.complete && i.naturalWidth === 0)
                    .map(i => i.getAttribute('src')),
                  menuVisible: toggle ? getComputedStyle(toggle).display !== 'none' : false,
                  menuSize: tr ? [Math.round(tr.width), Math.round(tr.height)] : null,
                  buttons: [...document.querySelectorAll('.button')]
                    .map(b => Math.round(b.getBoundingClientRect().height))
                };
            """)
            result["viewport"] = [width, height]
            print(json.dumps(result, sort_keys=True))
            if result["scrollWidth"] > result["innerWidth"] + 1 or result["offenders"]:
                failures.append(f"{width}px: horizontal overflow")
            if result["brokenImages"]:
                failures.append(f"{width}px: broken images {result['brokenImages']}")
            if width <= 390:
                if not result["menuVisible"]:
                    failures.append(f"{width}px: mobile menu control is not visible")
                elif result["menuSize"] and min(result["menuSize"]) < 44:
                    failures.append(f"{width}px: mobile menu touch target below 44px")
                if any(h < 44 for h in result["buttons"]):
                    failures.append(f"{width}px: primary button touch target below 44px")
            if args.screenshots:
                driver.save_screenshot(str(args.screenshots / f"viewport-{width}.png"))
        driver.quit()
    finally:
        if server:
            server.shutdown()
            server.server_close()

    if failures:
        print("Responsive check FAILED:")
        for item in failures:
            print(f"- {item}")
        return 1
    print("Responsive check passed for 320, 390, 768 and 1440 px widths.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
