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
- **Nicht migriert** (bewusst): 92 Medien-Anhänge (Bilder/GPX bleiben
  per Hotlink auf `https://hohetour.de/wp-content/uploads/…`
  referenziert), 6 Menüeinträge (ersetzt durch
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
  `convert_wp_part3.py` – Konverter (wird gemeinsam über
  `tools/run_convert.py` ausgeführt)
- `tools/run_convert.py` – führt die drei Teile in einem Prozess aus
- `_data/navigation.yml` – Hauptnavigation
- `_config.yml` – Minimal Mistakes, `locale: de-DE`, Feed/Sitemap

## Re-Build

```bash
bundle install
bundle exec jekyll build     # oder: task build
bundle exec jekyll serve     # oder: task serve
```
