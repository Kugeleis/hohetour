(function () {
  function initMaps() {
    if (typeof L === "undefined") {
      console.error("[leaflet-map] Leaflet (L) failed to load.");
      return;
    }

    var tileProviders = {
      default: {
        url: "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      },
      outdoors: {
        url: "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
        attribution:
          'Kartendaten: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, SRTM | Kartendarstellung: &copy; <a href="https://opentopomap.org">OpenTopoMap</a>',
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
      var centerAttr = el.dataset.center || "";
      var center = centerAttr && centerAttr !== "autolat,autolon"
        ? centerAttr.split(",").map(Number)
        : [50.80, 13.965];
      var zoom = parseInt(el.dataset.zoom, 10) || 11;
      var style = el.dataset.style || "default";
      var gpxUrl = el.dataset.gpx || "";

      var provider = tileProviders[style] || tileProviders["default"];
      var map = L.map(el).setView(center.length === 2 && !center.some(isNaN) ? center : [50.80, 13.965], zoom);

      L.tileLayer(provider.url, {
        attribution: provider.attribution,
        maxZoom: 19,
      }).addTo(map);

      // Render static markers if present
      var markers = [];
      try {
        markers = JSON.parse(el.dataset.markers || "[]");
      } catch (e) {
        console.error("[leaflet-map] invalid markers JSON:", e);
      }
      markers.forEach(function (m) {
        if (!m.coords) return;
        var marker = L.marker(m.coords).addTo(map);
        if (m.popup) marker.bindPopup(m.popup);
      });

      // If GPX URL is supplied, fetch and parse track points
      if (gpxUrl) {
        fetch(gpxUrl)
          .then(function (response) {
            if (!response.ok) throw new Error("HTTP " + response.status);
            return response.text();
          })
          .then(function (xmlText) {
            var parser = new DOMParser();
            var xmlDoc = parser.parseFromString(xmlText, "text/xml");
            var trkpts = xmlDoc.getElementsByTagName("trkpt");
            var latlngs = [];

            for (var i = 0; i < trkpts.length; i++) {
              var lat = parseFloat(trkpts[i].getAttribute("lat"));
              var lon = parseFloat(trkpts[i].getAttribute("lon"));
              if (!isNaN(lat) && !isNaN(lon)) {
                latlngs.push([lat, lon]);
              }
            }

            if (latlngs.length > 0) {
              var polyline = L.polyline(latlngs, {
                color: "#e63946",
                weight: 4,
                opacity: 0.85,
              }).addTo(map);

              map.fitBounds(polyline.getBounds(), { padding: [25, 25] });

              var startPt = latlngs[0];
              var endPt = latlngs[latlngs.length - 1];

              L.marker(startPt)
                .addTo(map)
                .bindPopup("<b>Start der Tour</b>");
              L.marker(endPt)
                .addTo(map)
                .bindPopup("<b>Ziel der Tour</b>");
            }
          })
          .catch(function (err) {
            console.warn("[leaflet-map] Failed to load GPX track:", gpxUrl, err);
          });
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initMaps);
  } else {
    initMaps();
  }
})();
