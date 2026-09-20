require 'json'
require 'cgi'

module Jekyll
  class MapTag < Liquid::Tag
    def initialize(tag_name, markup, tokens)
      super
    end

    def render(context)
      page = context.registers[:page]
      map_data = page['map']
      return '' unless map_data

      center = map_data['center']
      # Fail visibly instead of emitting broken JS when center is missing.
      unless center.is_a?(Array) && center.size == 2
        return '<!-- leaflet map: missing or invalid `map.center` ([lat, lng]) in front matter -->'
      end

      zoom = map_data['zoom'] || 13
      height = map_data['height'] || '450px'
      width = map_data['width'] || '100%'
      style = map_data['style'] || 'default'
      markers = map_data['markers'] || []

      # Escape values for safe embedding in HTML attributes.
      center_attr = CGI.escapeHTML(center.join(','))
      zoom_attr = CGI.escapeHTML(zoom.to_s)
      style_attr = CGI.escapeHTML(style.to_s)
      markers_attr = CGI.escapeHTML(JSON.generate(markers))
      css = CGI.escapeHTML("height: #{height}; width: #{width}; border-radius: 8px;")

      <<~HTML
        <div class="leaflet-map"
          data-center="#{center_attr}"
          data-zoom="#{zoom_attr}"
          data-style="#{style_attr}"
          data-markers="#{markers_attr}"
          style="#{css}">
        </div>
      HTML
    end
  end
end

Liquid::Template.register_tag('map', Jekyll::MapTag)

