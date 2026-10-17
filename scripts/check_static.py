#!/usr/bin/env python3
"""Small no-dependency smoke check for the static NOVA CORE page."""
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
        self.scripts = 0
        self.title = False
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                raise ValueError(f"Duplicate HTML id: {attrs['id']}")
            self.ids.add(attrs["id"])
        if tag == "script":
            self.scripts += 1
    def handle_data(self, data):
        if "NOVA CORE" in data:
            self.title = True

parser = CheckHTML()
parser.feed(html)
parser.close()

required = {
    "doneMetric", "netMetric", "taskCount", "progressBar", "progressFill",
    "goal", "limits", "makePlan", "planOutput", "business", "service",
    "price", "makeMessage", "messageOutput", "copyMessage", "sales",
    "costs", "calc", "net", "exportData", "resetTasks", "saveStatus",
}
missing = sorted(required - parser.ids)
if missing:
    raise SystemExit("Missing required element IDs: " + ", ".join(missing))
if parser.scripts != 1:
    raise SystemExit(f"Expected one inline script, found {parser.scripts}")

match = re.search(r"<script>(.*?)</script>", html, flags=re.S)
if not match:
    raise SystemExit("Inline JavaScript block not found")

with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8") as js:
    js.write(match.group(1))
    js.flush()
    result = subprocess.run(["node", "--check", js.name], text=True, capture_output=True)
    if result.returncode:
        raise SystemExit(result.stderr or result.stdout)

print("NOVA CORE smoke checks passed: required IDs present; inline JavaScript syntax valid.")
