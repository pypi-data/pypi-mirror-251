from jinja2 import Environment, FileSystemLoader
import importlib.resources as pkg_resources

def jinja_rendering(processing):
    with pkg_resources.path('ibl-tuning.ibldataset.utils', 'code_model.txt') as template_path:
        env = Environment(loader=FileSystemLoader(template_path.parent))
        template = env.get_template('code_model.txt')

    data = {'processing': processing}
    code_model = template.render(data)
    return code_model
