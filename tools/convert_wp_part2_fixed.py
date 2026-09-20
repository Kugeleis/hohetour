def localize_uploads(content):
    """Rewrite WP upload URLs to local Jekyll assets (baseurl-safe).

    Keeps the WP directory layout under assets/images/uploads/, e.g.
    wp-content/uploads/2020/07/05.jpg -> assets/images/uploads/2020/07/05.jpg
    Rendered as a `relative_url` tag so GitHub Pages (baseurl /hohetour)
    keeps working. Runs on every convert so `task convert` stays local.
    """
    if not content:
        return ""
    c = content
    c = re.sub(
        r"https?://(?:hohetour\.de|ht\.hosting139769\.a2e5e\.netcup\.net)/wp-content/uploads/([^\s\"'<>`,\)\]]+)",
        lambda m: "{{ '/assets/images/uploads/%s' | relative_url }}" % m.group(1).rstrip(".,;)"),
        c,
        flags=re.IGNORECASE,
    )
    c = re.sub(
        r"(?:\.\./)+wp-content/uploads/([^\s\"'<>`,\)\]]+)",
        lambda m: "{{ '/assets/images/uploads/%s' | relative_url }}" % m.group(1).rstrip(".,;)"),
        c,
    )
    return c


def clean_content(content):
    if not content:
        return ""
    c = content
    c = re.sub(r"<!--\s*/?wp:[^>]*-->", "", c)
    c = re.sub(r"\[mapsmarker[^\]]*\]",
               "\n\n> **Hinweis:** [Karte - OpenStreetMap-Karte der Tour (Original: hohetour.de)]\n\n", c)
    def osm_repl(m):
        inner = m.group(0)
        center = ""
        mc = re.search(r'map_center\s*=\s*"([^"]+)"', inner)
        if mc:
            center = mc.group(1).strip()
        mf = re.search(r'file_list\s*=\s*"([^"]+)"', inner)
        files = mf.group(1).strip() if mf else ""
        note = "Karte"
        if center:
            note += " (Zentrum: " + center + ")"
        if files:
            note += " - GPX: `" + files + "`"
        return "\n\n> **Hinweis:** [" + note + "]\n\n"
    c = re.sub(r"\[osm_map_v3[^\]]*\]", osm_repl, c)
    c = re.sub(r"\[wpforecast[^\]]*\]",
               "\n\n> **Hinweis:** [Wetter - Vorhersage Zinnwald, siehe wetter.com / altenberg.de]\n\n", c)
    c = re.sub(r"\[table[^\]]*\/?\]",
               "\n\n> **Hinweis:** [Tabelle - Datentabelle aus dem Original, nicht migriert]\n\n", c)
    c = re.sub(r"\[Best_Wordpress_Gallery[^\]]*\]",
               "\n\n> **Hinweis:** [Galerie - Bildergalerie im Original auf hohetour.de]\n\n", c)
    c = c.replace("[pagelist]", "(Sitemap des Originals - siehe Navigation)")
    c = c.replace("cke_show_border", "")
    c = localize_uploads(c)
    c = re.sub(
        r'<a(\s[^>]*?)href="https?://hohetour\.de/\?attachment_id=\d+"([^>]*?)>'
        r'(\s*<img\s[^>]*?src="(\{\{ \'/assets/images/uploads/[^\'"]+\' \| relative_url \}\})"[^>]*>)',
        lambda m: "<a%shref=\"%s\"%s>%s" % (m.group(1), m.group(4), m.group(2), m.group(3)),
        c,
        flags=re.IGNORECASE | re.DOTALL,
    )
    c = re.sub(
        r'\sdata-(?:full-url|link)="https?://hohetour\.de/\?attachment_id=\d+"',
        "",
        c,
        flags=re.IGNORECASE,
    )
    c = re.sub(r"\n{3,}", "\n\n", c)
    return c.strip() + "\n"

tree = ET.parse(str(XML))
items = tree.getroot().findall(".//item")
print("total items: %d" % len(items))

posts = []
pages = []
for it in items:
    ptype = text(it, "wp:post_type", NS)
    status = text(it, "wp:status", NS)
    if ptype not in ("post", "page"):
        continue
    if status != "publish":
        print("SKIP %s %s title=%r" % (ptype, status, text(it, "title")))
        continue
    title = text(it, "title") or "Ohne Titel"
    slug = text(it, "wp:post_name", NS) or slugify(title)
    slug = slugify(slug)
    date_raw = text(it, "wp:post_date", NS)
    try:
        dt = datetime.strptime(date_raw, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        dt = datetime.now()
    cats = [c.text for c in it.findall("category[@domain='category']") if c.text]
    tags = [c.text for c in it.findall("category[@domain='post_tag']") if c.text]
    comments = []
    for cm in it.findall("wp:comment", NS):
        approved = text(cm, "wp:comment_approved", NS)
        ctype = text(cm, "wp:comment_type", NS)
        if approved != "1":
            continue
        if ctype not in ("", "comment", "pingback", "trackback"):
            continue
        comments.append({
            "author": text(cm, "wp:comment_author", NS),
            "date": text(cm, "wp:comment_date", NS),
            "content": text(cm, "wp:comment_content", NS),
            "type": ctype or "comment",
        })
    entry = {"title": title, "slug": slug, "date": dt, "date_raw": date_raw,
             "content": text(it, "content:encoded", NS),
             "cats": cats, "tags": tags, "comments": comments,
             "post_id": text(it, "wp:post_id", NS)}
    (posts if ptype == "post" else pages).append(entry)

print("posts: %d pages: %d" % (len(posts), len(pages)))
for p in posts:
    print("  POST %s %s | %r cats=%s tags=%s cm=%d len=%d" % (
        p["date_raw"], p["slug"], p["title"][:50], p["cats"], p["tags"],
        len(p["comments"]), len(p["content"])))
for p in pages:
    print("  PAGE %s %s | %r len=%d" % (p["date_raw"], p["slug"], p["title"][:50], len(p["content"])))

POSTS_DIR.mkdir(exist_ok=True)
PAGES_DIR.mkdir(exist_ok=True)
