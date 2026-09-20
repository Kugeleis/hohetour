(function () {
  function initMaps() {
    if (typeof L === "undefined") {
      console.error("[leaflet-map] Leaflet (L) failed to load – check CDN script tag.");
      return;
    }

    var tileProviders = {
      default: {
        url: "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      },
      dark: {
        url: "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/">CARTO</a>',
      },
      light: {
        url: "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/">CARTO</a>',
      },
      satellite: {
        url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attribution: '&copy; <a href="https://www.esri.com/">Esri</a>',
      },
    };

    document.querySelectorAll(".leaflet-map").forEach(function (el) {
      var center = String(el.dataset.center || "")
        .split(",")
        .map(Number);
      var zoom = parseInt(el.dataset.zoom, 10) || 13;
      var style = el.dataset.style || "default";
      var markers = [];
      try {
        // NOTE: the browser already HTML-decodes data-* attributes,
        // so data-markers="[{&quot;...}]" arrives here as valid JSON.
        markers = JSON.parse(el.dataset.markers || "[]");
      } catch (e) {
        console.error("[leaflet-map] invalid markers JSON:", e);
      }

      if (center.length !== 2 || center.some(isNaN)) {
        console.error("[leaflet-map] invalid data-center, skipping map.");
        return;
      }

      var provider = tileProviders[style] || tileProviders["default"];

      var map = L.map(el).setView(center, zoom);

      L.tileLayer(provider.url, {
        attribution: provider.attribution,
        maxZoom: 19,
      }).addTo(map);

      markers.forEach(function (m) {
        if (!m.coords) return;
        var marker = L.marker(m.coords).addTo(map);
        if (m.popup) {
          marker.bindPopup(m.popup);
          if (m.open) {
            marker.openPopup();
          }
        }
      });
    });
  }

  // The script is loaded with `defer`, so the DOM is parsed already;
  // still guard for the case it is loaded without `defer`.
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initMaps);
  } else {
    initMaps();
  }
})();

