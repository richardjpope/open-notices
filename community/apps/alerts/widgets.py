from django.contrib.gis.forms import BaseGeometryWidget

class AlertAreaWidget(BaseGeometryWidget):
    template_name = 'alerts/widgets/alert_area.html'
    default_lon = 5
    default_lat = 47
    map_srid = 3857

    def __init__(self, attrs=None):
        super(AlertAreaWidget, self).__init__()
        for key in ('default_lon', 'default_lat'):
            self.attrs[key] = getattr(self, key)
        if attrs:
            self.attrs.update(attrs)