"""List every remote upload URL referenced from _posts/_pages + WP XML."""
import re
from pathlib import Path

ROOT = Path("/workspace")
targets = list((ROOT / "_posts").glob("*")) + list((ROOT / "_pages").glob("*"))
pat = re.compile(
    r"(?:https?://(?:hohetour\.de|ht\.hosting139769\.a2e5e\.netcup\.net)/wp-content/uploads/|(?:\.\./)+wp-content/uploads/)([^\s\"'<>`,\)\]]+)",
    re.IGNORECASE,
)
found = {}
for f in targets:
    if not f.is_file():
        continue
    t = f.read_text(encoding="utf-8", errors="replace")
    for m in pat.finditer(t):
        rel = m.group(1).strip().rstrip(".,;)")
        # strip trailing HTML entity remnants
        rel = re.sub(r"(&amp;|&quot;|&#\d+;)+$", "", rel)
        found.setdefault(rel, set()).add(f.name)

print(f"files scanned: {len(targets)}")
print(f"unique uploads: {len(found)}")
for rel in sorted(found):
    print(f"{rel}   <-- {', '.join(sorted(found[rel]))}")
