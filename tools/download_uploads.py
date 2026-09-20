"""Download every remote wp-content/uploads file into assets/images/uploads.

Keeps the WP directory structure (YYYY/MM/file, gpx/...) so local
paths map 1:1 to the original upload path.
Tries hohetour.de first, then the legacy staging host from the export.
"""
import urllib.request
import urllib.parse
from pathlib import Path

ROOT = Path("/workspace")
DEST = ROOT / "assets" / "images" / "uploads"
URLS = [
    "2017/01/vga_640-300x225.jpg",
    "2017/01/vga_640.jpg",
    "2018/02/Eis-300x154.jpg",
    "2020/07/05.jpg",
    "2020/07/15.jpg",
    "2020/07/16.jpg",
    "2020/07/17.jpg",
    "2020/07/18.jpg",
    "2020/07/2020-07-18_Hohe_Tour.gpx",
    "2020/07/21.jpg",
    "2020/07/24.jpg",
    "2020/07/25.jpg",
    "2020/07/27.jpg",
    "2020/07/31.jpg",
    "2020/07/32.jpg",
    "2020/07/33.jpg",
    "2020/07/35.jpg",
    "2020/07/36.jpg",
    "2020/07/38.jpg",
    "2020/07/41.jpg",
    "2020/07/43.jpg",
    "2020/07/45.jpg",
    "2020/07/46.jpg",
    "2020/07/51.jpg",
    "2020/07/53.jpg",
    "2020/07/54.jpg",
    "2020/07/56.jpg",
    "2020/07/57.jpg",
    "2020/07/58.jpg",
    "2020/07/59.jpg",
    "2020/07/60.jpg",
    "2020/07/62.jpg",
    "2020/07/66.jpg",
    "2020/07/photo5233500208493604283-1024x329.jpg",
    "2021/06/photo_200@21-06-2021_19-18-21-1-576x1024.jpg",
    "2021/06/photo_200@21-06-2021_19-18-21-1.jpg",
    "2021/06/photo_214@21-06-2021_19-18-25-576x1024.jpg",
    "2021/06/photo_214@21-06-2021_19-18-25.jpg",
    "2021/06/photo_216@21-06-2021_19-18-25-1024x576.jpg",
    "2021/06/photo_216@21-06-2021_19-18-25.jpg",
    "2021/06/photo_217@21-06-2021_19-18-25-576x1024.jpg",
    "2021/06/photo_217@21-06-2021_19-18-25.jpg",
    "2021/06/photo_219@21-06-2021_19-18-25-576x1024.jpg",
    "2021/06/photo_219@21-06-2021_19-18-25.jpg",
    "2021/06/photo_220@21-06-2021_19-18-28-1024x576.jpg",
    "2021/06/photo_220@21-06-2021_19-18-28.jpg",
    "2021/06/photo_223@21-06-2021_19-18-28-576x1024.jpg",
    "2021/06/photo_223@21-06-2021_19-18-28.jpg",
    "2021/06/photo_228@21-06-2021_19-18-28-1024x576.jpg",
    "2021/06/photo_228@21-06-2021_19-18-28.jpg",
    "2021/06/photo_231@21-06-2021_19-18-29-1024x576.jpg",
    "2021/06/photo_231@21-06-2021_19-18-29.jpg",
    "2021/06/photo_232@21-06-2021_19-18-29-1024x576.jpg",
    "2021/06/photo_232@21-06-2021_19-18-29.jpg",
    "2021/06/photo_233@21-06-2021_19-18-29-1024x576.jpg",
    "2021/06/photo_233@21-06-2021_19-18-29.jpg",
    "gpx/taubenteich.gpx",
    "gpx/zi-schoe.gpx",
]
HOSTS = [
    "https://hohetour.de/wp-content/uploads/",
    "https://ht.hosting139769.a2e5e.netcup.net/wp-content/uploads/",
]

ok = 0
failed = []
for rel in URLS:
    dest = DEST / rel
    if dest.exists() and dest.stat().st_size > 0:
        print(f"SKIP (exists) {rel}")
        ok += 1
        continue
    data = None
    used = None
    for host in HOSTS:
        url = host + urllib.parse.quote(rel, safe="/@")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "hohetour-migration/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            used = url
            break
        except Exception as e:  # noqa: BLE001 - report and try next host
            print(f"  miss {url}: {e}")
    if data is None:
        failed.append(rel)
        continue
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    ok += 1
    print(f"OK {rel} ({len(data)} bytes) <- {used}")

print(f"\ndownloaded/existing: {ok}/{len(URLS)}")
if failed:
    print("FAILED:")
    for rel in failed:
        print(f"  {rel}")
