from collections import Counter
import pkg_resources
from jinja2 import Environment, PackageLoader

# There's got to be a better way to do all this HTML bullshit...
# Can I use a framework here or something? https://materializecss.com/getting-started.html

pl = PackageLoader('tenzing', 'templates')
jinja2_env = Environment(lstrip_blocks=True, trim_blocks=True, loader=pl)

template_map = [
    'overview.html',
    'base.html',
    'list_composition.html',
    'html_wrapper.html',
    'frequency_table.html'
]


def get_template(template):
    return jinja2_env.get_template(template)


class renderable_config:
    def __init__(self, data_name, template_name, extra_configs={}):
        self.data_name = data_name
        self.template_name = template_name
        self.extra_configs = extra_configs

    @property
    def template(self):
        return get_template(self.template_name)

    def render(self, summary):
        data = {}
        data['data'] = summary.get(self.data_name)
        data.update(self.extra_configs)
        if 'frequencies' in data['data']:
            data['data']['frequencies'] = create_frequency_table(data['data']['frequencies'])
        res = self.template.render(data=data)
        return res


def create_frequency_table(frequencies, n=6):
    import heapq
    total = sum(frequencies.values())
    largest = heapq.nlargest(n, frequencies, key=frequencies.get)
    data = {item: frequencies[item] for item in largest}
    return get_template('frequency_table.html').render(data=data, total=total)


def traverse_config(config, summary):
    if isinstance(config, renderable_config):
        return config.render(summary)
    if isinstance(config, list):
        template = get_template('list_composition.html')
        data = [traverse_config(sub_config, summary) for sub_config in config]
        return template.render(data=data)
    elif isinstance(config, dict):
        raise Exception
    print('shouldnt get here')


def render_config(config, summary):
    base_template = get_template('base.html')
    html = {title: traverse_config(sub_config, summary) for title, sub_config in config.items()}
    return base_template.render(data=html)


class summary_report:
    def __init__(self, type_map, column_summary, general_summary, template=None):
        self.summary = {'general_summary': self.prettify(general_summary),
                        'type_counts': Counter(type_map.values()),
                        'column_summary': {k: self.prettify(v) for k, v in column_summary.items()},
                        'type_map': type_map}

        self.template = {'Overview': [renderable_config('general_summary', 'overview.html', {'title': 'Dataset Info'}),
                                      renderable_config('type_counts', 'overview.html', {'title': 'Variable types'})
                                      ],
                         'Variable Statistics': [renderable_config('/'.join(['column_summary', title]),
                                                                   'column_overview.html',
                                                                   {'title': title, 'subtitle': self.summary['type_map'][title]})
                                                 for title in self.summary['column_summary'].keys()]
                         }

    @staticmethod
    def prettify(dict_):
        return {key: v if not isinstance(v, float) else round(v, 2) for key, v in dict_.items()}

    def get(self, attr):
        for i, attr in enumerate(attr.split('/')):
            if i == 0:
                res = self.summary[attr]
            else:
                res = res[attr]
        return res

    def _repr_html_(self):
        return render_config(self.template, self)
