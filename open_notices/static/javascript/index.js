$(document).ready(function(){

  function extentToLonLat(extent){
    bottom_left = ol.proj.toLonLat([extent[0],extent[1]]);
    top_right = ol.proj.toLonLat([extent[2],extent[3]]);
    latlng_extent = [bottom_left[0], bottom_left[1], top_right[0], top_right[1]]
    return latlng_extent;
  }

  function updateURL(center, zoom){
    center = ol.proj.toLonLat(center);
    queryString = '?center=' + center.join(',');
    queryString += '&zoom=' + zoom;
    history.pushState({}, document.title, queryString)
  }

  //rotate intro text
  intro_text_example_count = 0;
  types = ['planning applications', 'licensing notices', 'parking suspensions', 'bin collections', 'food bank requirements'];
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

  //jiggle some controls about
  $('#q_label').addClass('show-for-sr');

  //map
  map = getBaseMap();
  var geoJSONFormat = new ol.format.GeoJSON();
  var vector = new ol.layer.Vector({
    source: new ol.source.Vector({
        format: new ol.format.GeoJSON(),
        url: function(extent) {
          extent = extentToLonLat(extent);
          return '/notices.geojson?bbox=' + extent.join(',');
        },
        strategy: ol.loadingstrategy.bbox
    }),
    style: getVectorStyle()
  });

  map.addLayer(vector);

  map.on('moveend', function(evt){
    zoom = evt.map.getView().getZoom();
    center = evt.map.getView().getCenter();
    updateURL(center, zoom);
  });

  //get location from url if present
  if(getUrlParameter('center') && getUrlParameter('zoom')){
    center = getUrlParameter('center').split(',').map(Number);
    center = ol.proj.fromLonLat(center);
    zoom = Number(getUrlParameter('zoom'));
    map.getView().setCenter(center);
    map.getView().setZoom(zoom);
  }

  map.on('click', function(evt) {
    feature = map.forEachFeatureAtPixel(evt.pixel,
      function(feature, layer) {
        return feature;
      });

    if (feature) {
      window.location.href = '/notices/' + feature.getId()
    }
  });


});