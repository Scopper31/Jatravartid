from config import model
from utilities.system_utilities import *
from utilities.terminal_utilities import *
import time


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


# анализ по системе
def analisys_of_project(path, question, gimiAI=True):

    project_structure = get_file_paths(path)
    all_content = []
    for path_to_file in project_structure:
        all_content.append(
            "path to file \n" + path_to_file + "\ncontent: \n" + read_file(path_to_file)
        )
    if not gimiAI:
        return "\n\n\n\n".join(all_content)
    prompt = (
        f"""
You are given a large project. Your task is to analyze it and then answer a question about it or help fix an error.

The project is:
"""
        + "\n\n\n\n".join(all_content)
        + f"""
The question is:

{question}

*Instructions:*

1. *Analyze the project:* 
    * Understand the project's structure, functionality, and purpose.
    * Identify key files, classes, functions, and dependencies.
    * Analyze the code for potential issues, such as bugs, security vulnerabilities, or performance bottlenecks.

2. *Answer the question or fix the error:*
    * If the question is a specific question about the project, provide a detailed and accurate answer.
    * If the question is related to an error, provide steps to fix the error or identify the root cause.
    * If the question requires understanding the project's functionality, describe how the project works and how the specific feature is implemented.

*Example:*

*Project:* A simple web application for managing a blog.
*Question:* "How can I add a new comment to a blog post?"

*Response:* 
    * "To add a new comment, you need to submit a POST request to the `/comments/` endpoint. The request should include a JSON payload with the following fields: `post_id`, `author`, `text`. The backend will then create a new comment object and associate it with the corresponding blog post." 

*Important:*
* If the code has syntax errors, try to understand the context and suggest corrections.
* If the code is complex, provide explanations and break down the logic into smaller steps.
* Be specific and provide accurate information.
* Use code snippets and examples to illustrate your answers.
"""
    )
    analysis_response = model.generate_content(prompt, stream=True)
    analysis_response.resolve()
    time.sleep(30)

    return analysis_response.text
