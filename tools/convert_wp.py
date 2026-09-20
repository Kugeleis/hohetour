"""Convert hohetour WordPress WXR export to Jekyll posts/pages."""
import re
import html
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
XML = ROOT / "hohetour.WordPress.2026-09-20.xml"
POSTS_DIR = ROOT / "_posts"
PAGES_DIR = ROOT / "_pages"

NS = {
    "wp": "http://wordpress.org/export/1.2/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
}

def text(el, tag, ns=None, default=""):
    if el is None:
        return default
    n = el.find(tag, ns) if ns else el.find(tag)
    if n is None or n.text is None:
        return default
    return n.text.strip()

def slugify(s):
    s = s.lower()
    for k, v in {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}.items():
        s = s.replace(k, v)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "post"

def yaml_quote(s):
    return '"' + s.replace('"', '\\"') + '"'
