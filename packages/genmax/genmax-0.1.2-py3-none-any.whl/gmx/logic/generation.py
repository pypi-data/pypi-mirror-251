import os
from jinja2 import Environment, FileSystemLoader
import yaml
import gmx.extensions as ex
from gmx.logic.common import CommonLogic

class GenerationLogic:
    def __init__(self) -> None:
        pass

    @staticmethod
    def generate(item):
        env = Environment(loader=FileSystemLoader(
            os.path.join(item['project_path'], 'templates')
            )
        )
        env.globals['lcase'] = ex.lcase
        env.globals['joinify'] = ex.joinify
        env.globals['pluralize'] = ex.pluralize
        env.globals['camel'] = ex.camel
        env.globals['kebab'] = ex.kebab
        env.globals['pascale'] = ex.pascale
        env.globals['dot'] = ex.dot
        env.globals['title'] = ex.title
        env.globals['snake'] = ex.snake
        env.globals['path'] = ex.path
        env.globals['uuid'] = ex.uuid
        env.globals['secret'] = ex.secret
        env.globals['secret_complex'] = ex.secret_complex
        env.globals['env'] = ex.env
        # Load the source data
        try:
            data_path = os.path.join(
                item['project_path'], 
                'data', 
                item['data']
            )
            with open(
                data_path
                ) as f:
                data = yaml.load(f, Loader=yaml.FullLoader)                
        except:
            print(f'Error reading {data_path}.')
        # Load the template
        template = env.get_template(item['template'])
        # Render the template with the source data
        output = template.render(data=data)
        CommonLogic.write_content_to_file(output, item['output'])