import os
import time
from config import model, folder_obj
from utilities.string_utilities import extract_blocks
from utilities.system_utilities import create_file


folder_name = folder_obj.folder_name


def develop(task):
    with open(f"""tests/{folder_name}/project_in_string_format.txt""") as file:
        code = file.read()

    prompt = f"""
        Please help me fix the following Python project. I want to make the following changes:

        {task}

        **Current project:**

        ```python
        {code}
        ```

        **Structure of multiple project visualisation:**
            - **File Names:** The marker `NAME_START` indicates the beginning of the file name and `NAME_END` indicates the end.  
            - **File Content:**  Each file's code is wrapped within the markers `#FILE_START` and `#FILE_END`.
            - **Package List:**  `#PACKAGES` marker followed by the space-separated list of package names at the end of the main file (`main.py`).

        **Output:**

        - **Corrected Code:** Provide the corrected version of the entire project code. Use the markers `#FILE_START` and `#FILE_END` to wrap each file's code.
        - **File Names:** Use the marker `NAME_START` to indicate the beginning of the file name and `NAME_END` to indicate the end. 
        markers are a mandatory part of the code
        "```python" , "```" are a mandatory part of the code

        **Example:**

        NAME_START game.py NAME_END

        ```python
        #FILE_START
        ... (corrected code for game.py) ...
        #FILE_END
        ```

        ... other files ...

        NAME_START main.py NAME_END

        ```python
        #FILE_START
        ... (corrected code for main.py) ...
        #PACKAGES pygame random
        #FILE_END
        ```
    """

    response = model.generate_content(prompt, stream=True)
    response.resolve()

    print(response.text)
    codes = extract_blocks(response.text, "#FILE_START", "#FILE_END")
    names = extract_blocks(response.text, "NAME_START", "NAME_END")

    try:
        with open(f"tests/{folder_name}/number.txt", "r") as file:
            number = int(file.read())
        number += 1
        with open(f"tests/{folder_name}/number.txt", "w") as file:
            file.write(str(number))

    except FileNotFoundError:
        with open(f"tests/{folder_name}number.txt", "w") as file:
            file.write("0")
            number = 0
    os.makedirs(f"tests/{folder_name}/correction{number}", exist_ok=True)
    for name, code in zip(names, codes):
        create_file(f"tests/{folder_name}/correction{number}", f"{name}", code)
    time.sleep(20)
