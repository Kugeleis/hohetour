# Hohe Tour – unterwegs zwischen Böhmen und Sachsen

Statische Jekyll-Seite als Nachfolgerin des WordPress-Blogs **hohetour.de**.
Theme: [Minimal Mistakes](https://mmistakes.github.io/minimal-mistakes/),
Sprache: Deutsch.

## Inhalte

Aus `hohetour.WordPress.2026-09-20.xml` (Stand September 2026) migriert:

- **13 Beiträge** (`_posts/`, 2004–2021) mit Kategorien/Tags, moderierte
  Kommentare als statisches Archiv am Beitragsende.
- **8 Seiten** (`_pages/`): `hallo-welt` (Tour-Übersicht), `sommer`,
  `winter`, `skitour-zinnwald-mueckentuermchen-schoena`,
  `ausruestung-anreise`, `gaestebuch-blog-seite` (WP-„Blog“),
  `links`, `wetter`.
- Dazu: `blog` (Übersicht), `archiv`, `kategorien`, `schlagworte`,
  `about`, `impressum`, deutsche Startseite (`index.markdown`),
  Navigation (`_data/navigation.yml`).

Bilder/GPX liegen lokal unter `assets/images/uploads/…` (aus
`wp-content/uploads/…` übernommen, Pfadstruktur beibehalten);
WP-Shortcodes (`mapsmarker`, `osm_map_v3`, `wpforecast`,
`table`, `Best_Wordpress_Gallery`) wurden zu Hinweisboxen. Details in
[`tools/README.md`](tools/README.md).

## Entwicklung

```bash
task install     # bundle install
task convert     # _posts/ + _pages/ aus dem WP-XML neu erzeugen
task build       # Jekyll-Build nach _site/
task serve       # http://localhost:4000 mit Live-Reload
task build:pages # Build wie GitHub Pages (baseurl /hohetour)
```
