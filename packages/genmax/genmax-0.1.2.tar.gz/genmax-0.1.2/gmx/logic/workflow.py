import os
import yaml
from gmx.logic.common import CommonLogic
from gmx.logic.generation import GenerationLogic
from gmx.logic.fileops import FileOpsLogic

class WorkFlowLogic:
    def __init__(self) -> None:
        pass

    def run_workflows(self, project_name: str, flows: list):
        project_path = os.path.join("gmx", project_name)
        project_path = CommonLogic.get_gmx_folder_path(project_path)
        for flow in flows:
            flow_path = os.path.join(project_path, 'flows', f'{flow}.yml')
            print(f'Processing Flow : {flow_path}.')
            # Load the items from the YAMl file
            try:
                with open(
                        flow_path
                    ) as f:
                    items = yaml.safe_load(f)
                    self._process_items(project_path, items)

                print(f'Flow Status: Done.\n')
            except Exception as e: 
                print(f'Flow processing failed.')
                print(f'Check Flow YAMl and filename(s).')
                continue

    def _process_items(self, project_path, items):

        # Loop through the items and generate the output files
        for item in items:
            item['project_path'] = project_path
            self._switch_action(
                item["action"],
                item
            )

    def _switch_action(self, argument, param):
        switcher = {
            "generate": GenerationLogic.generate,
            "write_to_file": FileOpsLogic.write_to_file,
        }
        # Get the function from switcher dictionary
        func = switcher.get(argument, self._default_action)
        # Execute the function and return its result
        return func(param)
    
    def _default_action(self, item):
        print("Unrecognized action.")


