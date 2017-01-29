$(document).ready(function(){
    var draw;

    //Hide the text area
    document.getElementById('id_location').setAttribute("hidden", true);
    document.getElementById('id_location-label').setAttribute("hidden", true);

    //Layers
    style = getVectorStyle();
    source = new ol.source.Vector({wrapX: false});
    vector = new ol.layer.Vector({source: source, style: style});

    //map
    var map = getBaseMap();
    map.addLayer(vector);
    map.addControl(new DrawControl({'type': 'Point'}));
    map.addControl(new DrawControl({'type': 'Polygon'}));
    map.addControl(new DrawControl({'type': 'LineString'}));

    //Geolocation
    geolocation = new ol.Geolocation({
            projection: map.getView().getProjection()
      });

    map.startDrawing = function(value){
        if (value !== 'None') {
          this.removeInteraction(draw);
          draw = new ol.interaction.Draw({
            source: source,
            type: (value),
            style: style
          });
          this.addInteraction(draw);
          draw.on('drawstart', function (event) {
            source.clear();
          });
        }
    }

    //store the geojson
    source.on('addfeature', function(){
        var writer = new ol.format.GeoJSON();
        var features = source.getFeatures();
        document.getElementById('id_location').value = writer.writeGeometry(features[0].getGeometry());
    });

});