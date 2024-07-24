from config import model


def generate_alias(task):
    alias_response = model.generate_content(
        f"output alias for task, that will be the name of folder with the project: {task}. output only alias literally in few words without wrapping in \"**\"",
        stream=True)  # Generate alias from task
    alias_response.resolve()
    return '_'.join(alias_response.text.split())