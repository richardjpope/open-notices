$(document).ready(function(){

    //Hide the text area
    document.getElementById('id_location').setAttribute("hidden", true);
    document.getElementById('id_location-label').setAttribute("hidden", true);

    map = getBaseMap();
    style = getVectorStyle();
    source = new ol.source.Vector({wrapX: false});
    vector = new ol.layer.Vector({source: source, style: style});

    map.addLayer(vector);

    //drawing
    interaction = new ol.interaction.Draw({
      source: source,
      type: 'Polygon',
      freehand: true,
      style: style
    });

    interaction.on('drawstart', function (event) {
        source.clear();
    });
    map.addInteraction(interaction);

    //store the geojson
    source.on('addfeature', function(){
        var writer = new ol.format.GeoJSON();
        var features = source.getFeatures();
        document.getElementById('id_location').value = writer.writeGeometry(features[0].getGeometry());
    });

});