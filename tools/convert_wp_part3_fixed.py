def excerpt_of(body):
    plain = re.sub(r"<[^>]+>", " ", body)
    plain = html.unescape(re.sub(r"\s+", " ", plain)).strip()
    if len(plain) > 200:
        return plain[:197] + "..."
    return plain

# Die WP-Seite mit Slug "blog" wuerde mit blog.md (Posts-Uebersicht)
# kollidieren. Sie wird dauerhaft als Gaestebuch-Seite abgelegt.
PAGE_OVERRIDES = {
    "blog": {"fname": "gaestebuch-blog-seite.md",
             "permalink": "/gaestebuch-blog-seite/",
             "title": "Aus dem Gästebuch"},
}

for p in posts:
    fname = "%s-%s.markdown" % (p["date"].strftime("%Y-%m-%d"), p["slug"])
    body = clean_content(p["content"])
    ex = excerpt_of(body)
    lines = ["---", "layout: single",
             "title: " + yaml_quote(p["title"]),
             "date: " + p["date"].strftime("%Y-%m-%d %H:%M:%S +0100"),
             "slug: " + p["slug"],
             "wordpress_id: " + p["post_id"],
             "author_profile: false", "read_time: true",
             "toc: true", 'toc_label: "Inhalt"',
             "comments: false", "share: true"]
    if p["cats"]:
        lines.append("categories:")
        for c in p["cats"]:
            lines.append("  - " + yaml_quote(c))
    if p["tags"]:
        lines.append("tags:")
        for t in p["tags"]:
            lines.append("  - " + yaml_quote(t))
    if ex:
        lines.append("excerpt: " + yaml_quote(ex))
    lines += ["---", ""]
    out = "\n".join(lines) + body
    if p["comments"]:
        out += "\n\n---\n\n## Kommentare aus dem Original-Blog\n\n"
        out += "_%d Kommentar(e) von hohetour.de (archiviert)._ \n\n" % len(p["comments"])
        for cm in p["comments"]:
            label = "Pingback" if cm["type"] in ("pingback", "trackback") else "Kommentar"
            author = cm["author"] or "Anonym"
            content = (cm["content"] or "").strip().replace("\n", "\n> ")
            out += "\n**%s** - *%s* - _%s_\n\n> %s\n\n" % (author, cm["date"], label, content)
    (POSTS_DIR / fname).write_text(out, encoding="utf-8")
    print("WROTE post " + fname)

for p in pages:
    ov = PAGE_OVERRIDES.get(p["slug"], {})
    fname = ov.get("fname", "%s.md" % p["slug"])
    permalink = ov.get("permalink", "/" + p["slug"] + "/")
    title = ov.get("title", p["title"])
    body = clean_content(p["content"])
    ex = excerpt_of(body)
    lines = ["---", "layout: single",
             "title: " + yaml_quote(title),
             "permalink: " + permalink,
             "author_profile: false", "toc: true",
             "wordpress_id: " + p["post_id"]]
    if ex:
        lines.append("excerpt: " + yaml_quote(ex))
    lines += ["---", ""]
    out = "\n".join(lines) + body
    if p["comments"]:
        out += "\n\n---\n\n## Kommentare aus dem Original-Blog\n\n"
        for cm in p["comments"]:
            author = cm["author"] or "Anonym"
            content = (cm["content"] or "").strip().replace("\n", "\n> ")
            out += "\n**%s** - *%s*\n\n> %s\n\n" % (author, cm["date"], content)
    target = PAGES_DIR / fname
    # Alte Datei vom Slug-Namen entfernen, falls ein Override greift
    # (z. B. _pages/blog.md aus frueheren Konverter-Laeufen).
    legacy = PAGES_DIR / ("%s.md" % p["slug"])
    if legacy != target and legacy.exists():
        legacy.unlink()
        print("REMOVED legacy " + legacy.name)
    target.write_text(out, encoding="utf-8")
    print("WROTE page " + fname)
