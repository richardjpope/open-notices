  function staticMap(map_id, geojson_url){

    //map
    var geoJSONFormat = new ol.format.GeoJSON();
    var source = new ol.source.Vector({
          format: new ol.format.GeoJSON(),
          url: geojson_url
      });
    var raster = new ol.layer.Tile({source: new ol.source.Stamen({layer: 'toner'})});
    var vector = new ol.layer.Vector({
      source: source,
      style: new ol.style.Style({
          stroke: new ol.style.Stroke({
              color: '#ff0000',
              width: 6
          }),
          image: new ol.style.Circle({
                          radius: 7,
                          fill: new ol.style.Fill({
                              color: '#ff0000',
                          })
                      })
      })
    });
    var map = new ol.Map({
        layers: [raster, vector],
        target: map_id,
        controls: ol.control.defaults({zoom:false, rotate:false}),
        interactions: ol.interaction.defaults({mouseWheelZoom:false, altShiftDragRotate:false, doubleClickZoom: false, keyboard:false, shiftDragZoom:false, dragPan:false, pinchRotate:false, pinchZoom:false}),
        view: new ol.View({center: [0, 4600000],zoom: 2})
    });

    source.on('change', function() {
      if (source.getState() == 'ready') {
        buffer_size = 250; //no idea what the units are here!
        buffered_extent = ol.extent.buffer(source.getExtent(), buffer_size);
        map.getView().fit(buffered_extent, map.getSize());
      }
    });
  }