from collections import Counter
import pkg_resources
from jinja2 import Environment, PackageLoader
import yaml

# There's got to be a better way to do all this HTML bullshit...
# Can I use a framework here or something? https://materializecss.com/getting-started.html

pl = PackageLoader('tenzing', 'templates')
jinja2_env = Environment(lstrip_blocks=True, trim_blocks=True, loader=pl)

template_map = [
    'overview.html',
    'base.html',
    'list_composition.html',
    'html_wrapper.html'
]


def get_template(template):
    return jinja2_env.get_template(template)


def _get_default_config():
    _resource_path = 'templates/default_report_config.yaml'
    _config_file = pkg_resources.resource_filename(__name__, _resource_path)
    string_res = pkg_resources.resource_string(__name__, _resource_path)
    default_template = yaml.load(string_res, Loader=yaml.FullLoader)
    return process_yaml_template(default_template)


def traverse_config(config, summary):
    if isinstance(config, list):
        list_cmp_template = get_template('list_composition.html')
        return list_cmp_template.render(data=[traverse_config(subconfig, summary) for subconfig in config])
    elif isinstance(config, dict):
        if config.get('is_abstract_variable', False):
            list_cmp_template = get_template('list_composition.html')
            html_list = []
            for title, val_dict in summary.get(config['data']).items():
                new_data = {'title': summary.get('col_type_map')[title], 'data': val_dict}
                html = get_template(config['template']).render(data=new_data)
                new_data['title'] = title
                new_data['data'] = html

                html_list.append(new_data)

            result = list_cmp_template.render(data=html_list)
            return result

        elif 'template' in config and 'data' in config:
            template = get_template(config['template'])
            data = config.copy()
            data.pop('template')
            data['data'] = summary.get(config['data'])
            return template.render(data=data)
        else:
            return {key: traverse_config(value, summary) for key, value in config.items()}


def process_yaml_template(template):
    if isinstance(template, list):
        return [process_yaml_template(subtemp) for subtemp in template]
    elif isinstance(template, dict):
        new_template = {}
        for key, values in template.items():
            if 'template' in values and 'data' in values:
                values.update({'title': key})
                new_template[key] = values
            else:
                new_template[key] = process_yaml_template(values)
        return new_template


class summary_report:
    def __init__(self, col_type_map, column_summary, general_summary, template=None):
        self.column_summary = {k: self.prettify(v) for k, v in column_summary.items()}
        self.general_summary = self.prettify(general_summary)
        self.col_type_map = col_type_map
        self.type_counts = Counter(self.col_type_map.values())
        self.template = _get_default_config() if template is None else template
        self.html = self.generate_html()

    @staticmethod
    def prettify(dict_):
        return {key: v if not isinstance(v, float) else round(v, 2) for key, v in dict_.items()}

    def generate_html(self):
        base_template = get_template('base.html')
        data = traverse_config(self.template, self)
        html_output = base_template.render(data=data)
        return html_output

    def get(self, attr):
        return getattr(self, attr)

    def _repr_html_(self):
        return self.html
