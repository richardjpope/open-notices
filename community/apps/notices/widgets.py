import json
from django.forms import Widget
from django.template import loader

class DataWidget(Widget):
    template_name = 'notices/widgets/data.html'

    def __init__(self, attrs=None, empty_count=5):
        super(DataWidget, self).__init__()
        self.empty_count = empty_count

    def render(self, name, value, attrs=None):
        items = []
        try:
            json_data = json.loads(value)
            for k, v in json_data.items():
                items.append((k, v))
            while len(items) <= self.empty_count:
                items.append(('', ''))
        except TypeError:
            pass
        context = {'name': name, 'value':  items}
        return loader.render_to_string(self.template_name, context)

    def value_from_datadict(self, data, files, name):
        counter = 0
        result = {}
        end = False
        while end == False:
            try:
                if data['%s_key_%d' % (name, counter)]:
                    result[data['%s_key_%d' % (name, counter)]] = data['%s_value_%d' % (name, counter)]
                counter +=1
            except KeyError:
                end = True
        return result
