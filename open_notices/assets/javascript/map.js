

DrawControl = function(opt_options) {

    options = opt_options || {};

    button = $('<button type="button">Draw ' + options['type'].toLowerCase() +'</button>').get()[0];

    var this_ = this;
    var handleDrawLocation = function(event) {
        this_.getMap().startDrawing(event.data['type']);
    };
    
    $(button).on('click',  options, handleDrawLocation);
    $(button).on('touchstart', options, handleDrawLocation);

    control = $('<div class="draw-' + options['type'].toLowerCase() + ' ol-unselectable ol-control"></div>')
    control.append(button);

    ol.control.Control.call(this, {
      element: control.get()[0],
      target: options.target
    });

  };
ol.inherits(DrawControl, ol.control.Control);


ClearSelectionControl = function(opt_options) {

    options = opt_options || {};

    button = document.createElement('button');
    button.innerHTML = 'Clear';
    button.setAttribute('type', 'button');

    var this_ = this;
    var handleClearSelection = function() {
      layer = this_.getMap().getLayers().getArray()[1]
      source = layer.getSource();
      source.clear();
      return false;
    };

    button.addEventListener('click', handleClearSelection, false);
    button.addEventListener('touchstart', handleClearSelection, false);

    var element = document.createElement('div');
    element.className = 'clear-selection ol-unselectable ol-control';
    element.appendChild(button);

    ol.control.Control.call(this, {
      element: element,
      target: options.target
    });

  };

ol.inherits(ClearSelectionControl, ol.control.Control);

  //Location control
  LocateControl = function(opt_options) {

      options = opt_options || {};

      button = document.createElement('button');
      button.innerHTML = '&#8982;';
      button.setAttribute('type', 'button');
      geolocation = false

      var this_ = this;
      var handleLocate = function() {
        
        if (navigator.geolocation) {
          if (geolocation == false){
            geolocation = new ol.Geolocation({
              projection: this_.getMap().getView().getProjection()
            });

            geolocation.on('change', function() {
              this_.getMap().getView().setCenter(geolocation.getPosition());
              this_.getMap().getView().setZoom(15);
            });

            geolocation.on('error', function(error) {
              alert('Unable to get your location')
            });
          }

          geolocation.setTracking(false);
          geolocation.setTracking(true);
          return false;
        };
      }

      button.addEventListener('click', handleLocate, false);
      button.addEventListener('touchstart', handleLocate, false);

      var element = document.createElement('div');
      element.className = 'ol-locate ol-unselectable ol-control';
      element.appendChild(button);

      ol.control.Control.call(this, {
        element: element,
        target: options.target
      });

    };

  ol.inherits(LocateControl, ol.control.Control);

function getVectorStyle(){
  var style = new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: '#ff0000',
            width: 3
        }),
        image: new ol.style.Circle({
                        radius: 7,
                        fill: new ol.style.Fill({
                            color: '#ff0000'
                        })
                    })
    });
  return style
}
function getBaseMap(){
    raster = new ol.layer.Tile({source: new ol.source.Stamen({layer: 'toner'})});
    view = new ol.View({center: ol.proj.fromLonLat([0.1278, 51.5074]), zoom: 10})

    var map = new ol.Map({
        target: 'map',
        layers: [raster],
        interactions: ol.interaction.defaults({mouseWheelZoom:false}),
        view: view,
        controls: ol.control.defaults({zoom:true, rotate:false}).extend([
            new LocateControl()
          ]),
    });
    geocoder = new Geocoder('nominatim', {
        provider: 'pelias',
        key: 'mapzen-VoiExtQ',
        lang: 'en-GB', //en-US, fr-FR
        placeholder: 'Search',
        limit: 5,
        keepOpen: false,
        autoComplete: false,
        countrycodes: 'gb',
        autoCompleteMinLength: 1,
        preventDefault: true,
        targetType: 'text-input'
      });
      map.addControl(geocoder);

      geocoder.on('addresschosen', function(evt){
        map.getView().setCenter(evt.coordinate);
      });

      //move the controls about to fit device
      intro_position = $('#intro').position()
      $('.ol-zoom').css('top', (intro_position['top'] - 200) + 'px');
      $('.ol-locate').css('top', (intro_position['top'] - 120) + 'px');

      return map
}
