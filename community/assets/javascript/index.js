$(document).ready(function(){


  //rotate intro text
  intro_text_example_count = 0;
  types = ['planning applications', 'licensing notices', 'parking suspensions', 'bin collections'];
  setInterval(function(){
    $('#intro-text-examples').fadeOut(300, function(){
      $('#intro-text-examples').html(types[intro_text_example_count]);  
      $('#intro-text-examples').fadeIn(300);
      
      if (intro_text_example_count < types.length - 1) {
        intro_text_example_count ++;
      } else {
        intro_text_example_count = 0;
      }

    });
  }, 2000);

  //map
  var geoJSONFormat = new ol.format.GeoJSON();
  
  raster = new ol.layer.Tile({source: new ol.source.OSM()});
  var vector = new ol.layer.Vector({
    source: new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        url: 'http://localhost:8000/notices.geojson'
    }),
    style: new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: '#000000',
            width: 1.5
        }),
        image: new ol.style.Circle({
                        radius: 7,
                        fill: new ol.style.Fill({
                            color: 'black'
                        })
                    })
    })
});

  view = new ol.View({center: [0, 4600000],zoom: 2})
  geolocation = new ol.Geolocation({
        projection: view.getProjection()
      });

  var map = new ol.Map({
      layers: [raster, vector],
      target: 'map',
      interactions: ol.interaction.defaults({mouseWheelZoom:false}),
      view: view
  });

  geolocation.on('change', function() {
      map.getView().setCenter(geolocation.getPosition());
      map.getView().setZoom(15);
      loading.hide();
  });

  geolocation.on('error', function(error) {
    loading.hide();
    alert('Unable to get your location')
  });

  //geo-location
  if (navigator.geolocation) {
    div = $('<div></div>')
    loading = $('<img id="loading-geolocation">')
    loading.attr("src", STATIC_URL + 'images/loading-small.gif');
    loading.hide();

    a = $('<a href="#">Use my location</a>');
    a.click(function(){
      geolocation.setTracking(false);
      geolocation.setTracking(true);
      $('#loading-geolocation').show();
    });
    div.append(a);
    div.append(loading);
    $('#intro form').append(div);
  }

  //Popup
  popup_html = $('<div id="popup" class="ol-popup map-popup">HELLO</div>');
  $('#map').append(popup_html);
  popup = new ol.Overlay({element: document.getElementById('popup')});
  map.addOverlay(popup);

  map.on('click', function(evt) {
    feature = map.forEachFeatureAtPixel(evt.pixel,
      function(feature, layer) {
        return feature;
      });
    element = popup.getElement();
    if (feature) {
      $(element).html('<a href="/notices/' + feature.getId() + '">' + feature.getProperties()['title'] + '</a>');
      $(element).show();
      centroid = ol.extent.getCenter(feature.getGeometry().getExtent());
      pan = ol.animation.pan({duration: 200,source:(view.getCenter())});
      popup.setPosition(centroid);
      map.beforeRender(pan);
      map.getView().setCenter(centroid);

    } else {
      $(element).hide();
    }
  });

});