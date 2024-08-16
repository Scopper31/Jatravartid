from config import model
from utilities.system_utilities import *


def generate_alias(task, bar, *arg, **kwargs):

    try:
        alias_response = model.generate_content(
            f'output alias for task, that will be the name of folder with the project: {task}. Alias should be suitable for folder name. output only alias literally in few words without wrapping in "**"',
            stream=True,
        )  # Generate alias from task
        alias_response.resolve()
        main_text = "_".join(alias_response.text.split())
        bar()
        add_to_process("alias", "Done")
    except Exception as e:
        print(f"Error in generating or processing prompt: {e}")
        add_to_log("utilities.neuro_utilities/generate_alias", e)
        return None

    return main_text
