#!/usr/bin/env python3
"""No-dependency smoke checks for NOVA CORE HTML, JavaScript and PWA assets."""
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "NOVA-CORE" / "index.html"
html = PAGE.read_text(encoding="utf-8")

class CheckHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                raise ValueError(f"Duplicate HTML id: {attrs['id']}")
            self.ids.add(attrs["id"])

parser = CheckHTML()
parser.feed(html)
parser.close()

required = {
    "doneMetric", "netMetric", "taskCount", "progressBar", "progressFill",
    "goal", "limits", "makePlan", "planOutput", "business", "service",
    "price", "makeMessage", "messageOutput", "copyMessage", "sales",
    "costs", "calc", "net", "exportData", "resetTasks", "saveStatus",
    "authEmail", "authPassword", "signIn", "signUp", "signOut",
    "cloudPlan", "cloudSync", "cloudOutput", "authStatus",
    "recipientId", "socialMessage", "sendSocialMessage", "refreshSocialMessages",
    "socialOutput", "paymentAmount", "paymentPurpose", "createPaymentIntent",
    "paymentOutput",
}
missing = sorted(required - parser.ids)
if missing:
    raise SystemExit("Missing required element IDs: " + ", ".join(missing))

for asset in (
    ROOT / "NOVA-CORE" / "manifest.webmanifest",
    ROOT / "NOVA-CORE" / "sw.js",
    ROOT / "NOVA-CORE" / "icons" / "nova-192.svg",
    ROOT / "NOVA-CORE" / "icons" / "nova-512.svg",
):
    if not asset.is_file():
        raise SystemExit(f"Missing PWA asset: {asset.relative_to(ROOT)}")

matches = re.findall(r"<script\b([^>]*)>(.*?)</script\s*>", html, flags=re.S | re.I)
inline_scripts = [
    body for attrs, body in matches
    if not re.search(r"\bsrc\s*=", attrs, flags=re.I) and body.strip()
]
if not inline_scripts:
    raise SystemExit("Inline JavaScript blocks not found")

for index, source in enumerate(inline_scripts, start=1):
    with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8") as js:
        js.write(source)
        js.flush()
        result = subprocess.run(["node", "--check", js.name], text=True, capture_output=True)
        if result.returncode:
            raise SystemExit(f"Inline JavaScript block {index} is invalid:\n" + (result.stderr or result.stdout))

print(f"NOVA CORE smoke checks passed: {len(required)} required IDs; PWA assets present; {len(inline_scripts)} inline JavaScript blocks syntax-valid.")
