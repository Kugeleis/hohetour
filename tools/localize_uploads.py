"""Rewrite remote wp-content/uploads links in _posts/_pages to local assets.

Local target: /assets/images/uploads/<rel> (same layout as WP uploads,
e.g. 2020/07/05.jpg, gpx/zi-schoe.gpx).

Links become Jekyll liquid tags so `baseurl` (GitHub Pages project site)
keeps working:
    {{ '/assets/images/uploads/2020/07/05.jpg' | relative_url }}

Handles:
  - https://hohetour.de/wp-content/uploads/<rel>
  - https://ht.hosting139769.a2e5e.netcup.net/wp-content/uploads/<rel>
  - relative  ../../wp-content/uploads/<rel>  (legacy converter output)
Idempotent: already-localized tags are left alone.
"""
import re
from pathlib import Path

ROOT = Path("/workspace")
TARGETS = list((ROOT / "_posts").glob("*")) + list((ROOT / "_pages").glob("*"))

REMOTE = re.compile(
    r"https?://(?:hohetour\.de|ht\.hosting139769\.a2e5e\.netcup\.net)/wp-content/uploads/",
    re.IGNORECASE,
)
RELATIVE = re.compile(r"(?:\.\./)+wp-content/uploads/")

LOCAL_TAG = "{{ '/assets/images/uploads/%s' | relative_url }}"


def repl_remote(m):
    return LOCAL_TAG % m.group(1)


changed_files = 0
changed_refs = 0
for f in TARGETS:
    if not f.is_file():
        continue
    t = f.read_text(encoding="utf-8")
    orig = t
    # remote absolute URLs (capture the path after uploads/)
    t, n1 = re.subn(
        r"https?://(?:hohetour\.de|ht\.hosting139769\.a2e5e\.netcup\.net)/wp-content/uploads/([^\s\"'<>`,\)\]]+)",
        lambda m: LOCAL_TAG % m.group(1).rstrip(".,;)"),
        t,
        flags=re.IGNORECASE,
    )
    # legacy relative URLs
    t, n2 = re.subn(
        r"(?:\.\./)+wp-content/uploads/([^\s\"'<>`,\)\]]+)",
        lambda m: LOCAL_TAG % m.group(1).rstrip(".,;)"),
        t,
    )
    if t != orig:
        f.write_text(t, encoding="utf-8")
        changed_files += 1
        changed_refs += n1 + n2
        print(f"REWROTE {f.name}: {n1 + n2} refs")

print(f"\nfiles changed: {changed_files}, refs rewritten: {changed_refs}")

# safety: report any leftovers pointing at WP uploads
leftover = []
for f in TARGETS:
    if not f.is_file():
        continue
    t = f.read_text(encoding="utf-8")
    if "wp-content/uploads" in t:
        leftover.append(f.name)
if leftover:
    print("LEFTOVER wp-content/uploads in:", ", ".join(leftover))
else:
    print("OK: no wp-content/uploads references left in _posts/_pages")
