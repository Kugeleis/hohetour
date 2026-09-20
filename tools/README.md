# Hohe Tour — WordPress → Jekyll Migration
# Quelle: hohetour.WordPress.2026-09-20.xml (WP 7.1.1, Export 2026-09-20)

Diese Jekyll-Seite ist aus dem WordPress-Export der Domain
**hohetour.de** („Hohe Tour – unterwegs zwischen Böhmen und Sachsen“)
erzeugt worden.

## Was wurde migriert?

- **13 Beiträge** (`_posts/`, 2004–2021): alle `post`-Items mit Status
  `publish`, inkl. Kategorien, Tags und moderierter Kommentare
  (als statisches Archiv am Ende des jeweiligen Beitrags).
- **8 Seiten** (`_pages/`, Permalinks `/slug/`): Startseite
  (`hallo-welt`), Sommer, Winter, Skitour-Route, Ausrüstung & Anreise,
  Blog, Links, Wetter.
- **Nicht migriert** (bewusst): 92 Medien-Anhänge als eigene
  Inhaltsseiten (ihre Dateien aus `wp-content/uploads/…` liegen lokal
  unter `assets/images/uploads/…` mit gleicher Pfadstruktur und werden
  aus Beiträgen/Seiten verlinkt), 6 Menüeinträge (ersetzt durch
  `_data/navigation.yml`), Entwürfe/Private Seiten
  (`Forum`, `Datenschutzerklärung`, `Praktische Autos`),
  `bwg_gallery`-Beitrag.

## Shortcodes / alte Plugins

WordPress-Shortcodes gibt es in Jekyll nicht. Sie wurden durch
Hinweisboxen ersetzt:

| Original | Ersatz |
|---|---|
| `[mapsmarker …]` | Hinweisbox „Karte (Original: hohetour.de)“ |
| `[osm_map_v3 …]` | Hinweisbox mit Zentrum + GPX-Pfad |
| `[wpforecast …]` | Hinweisbox Wetter (wetter.com / altenberg.de) |
| `[table …]` | Hinweisbox Datentabelle |
| `[Best_Wordpress_Gallery …]` | Hinweisbox Bildergalerie |

## Dateien

- `tools/convert_wp.py` + `convert_wp_part2_fixed.py` +
  `convert_wp_part3_fixed.py` – Konverter (wird gemeinsam über
  `tools/run_convert.py` ausgeführt; `clean_content()` schreibt
  `wp-content/uploads`-Links dabei direkt auf lokale
  `assets/images/uploads/`-Pfade mit `relative_url` um)
- `tools/run_convert.py` – führt die drei Teile in einem Prozess aus
- `tools/download_uploads.py` – lädt alle in `_posts/`/`_pages/`
  referenzierten `wp-content/uploads`-Dateien (Stand der Migration:
  58 Dateien, ~11 MB) nach `assets/images/uploads/` (gleiche
  Pfadstruktur wie in WordPress)
- `tools/localize_uploads.py` – schreibt Remote-Upload-Links in
  `_posts/`/`_pages/` auf lokale `relative_url`-Tags um (idempotent)
- `tools/localize_attachments.py` – hängt Galerie-Anker von
  `?attachment_id=`-Seiten auf das lokale Bild um und entfernt
  `data-full-url`/`data-link`-Reste (idempotent)
- `tools/collect_urls.py` – listet alle referenzierten Upload-Pfade
  mit den Dateien, die sie verwenden (Prüf-/Audit-Hilfe)
- `_data/navigation.yml` – Hauptnavigation
- `_config.yml` – Minimal Mistakes, `locale: de-DE`, Feed/Sitemap

## Re-Build

```bash
bundle install
bundle exec jekyll build     # oder: task build
bundle exec jekyll serve     # oder: task serve
```
