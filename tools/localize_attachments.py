"""Point WP attachment-page anchors at the local image they wrap.

After localize_uploads.py, gallery items still look like:
  <a href="https://hohetour.de/?attachment_id=243"><img src="LOCAL ...">
The image itself is local, but the click-through goes to WordPress.
This rewrites such anchors to the wrapped <img> local URL, so no
click leads back to the WP site. Idempotent.
"""
import re
from pathlib import Path

ROOT = Path("/workspace")
TARGETS = list((ROOT / "_posts").glob("*")) + list((ROOT / "_pages").glob("*"))

# <a ... href="https://hohetour.de/?attachment_id=N"><img ... src="LOCAL" ...>
pat = re.compile(
    r'<a(\s[^>]*?)href="https?://hohetour\.de/\?attachment_id=\d+"([^>]*?)>'
    r'(\s*<img\s[^>]*?src="(\{\{ \'/assets/images/uploads/[^\'"]+\' \| relative_url \}\})"[^>]*>)',
    re.IGNORECASE | re.DOTALL,
)
# stale WP metadata on gallery <img> tags (href/src already local)
meta = re.compile(
    r'\sdata-(?:full-url|link)="https?://hohetour\.de/\?attachment_id=\d+"',
    re.IGNORECASE,
)

total_files = 0
total_refs = 0
for f in TARGETS:
    if not f.is_file():
        continue
    t = f.read_text(encoding="utf-8")
    t, n1 = pat.subn(lambda m: f"<a{m.group(1)}href=\"{m.group(4)}\"{m.group(2)}>{m.group(3)}", t)
    t, n2 = meta.subn("", t)
    if n1 + n2:
        f.write_text(t, encoding="utf-8")
        total_files += 1
        total_refs += n1 + n2
        print(f"REWROTE {f.name}: {n1} attachment anchors, {n2} metadata attrs")

print(f"\nfiles changed: {total_files}, rewrites: {total_refs}")
