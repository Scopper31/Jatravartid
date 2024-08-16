# -*- coding: utf-8 -*-
# pip install google-generativeai
import subprocess

from utilities import *
from project_debug import *
from config import folder_obj
from alive_progress import alive_bar


def solve_task(task_):
    # technical writer

    analysis_prompt = f"""
        You are a highly skilled technical writer, tasked with crafting a comprehensive technical assignment for a large, complex project. Your goal is to provide clear and detailed instructions for the programmer, ensuring they understand the project's requirements and can successfully implement the solution.

        **Task:** {task_}

        **Technical Assignment:**

        1. **Project Overview:**
            - Provide a concise and clear explanation of the overall project goal.
            - Define the scope of the task and its role within the larger project. 
            - Outline any constraints or limitations that the programmer needs to consider.
        2. **Technical Requirements:**
            - Detail the specific functionalities the program should provide.
            - Specify the input and output formats for the program.
            - Define the expected user interactions and program behavior. 
        3. **Implementation Guidelines:**
            - Describe the recommended programming language and libraries for the task.
            - Explain any specific algorithms, data structures, or design patterns required for the implementation. 
            - Provide suggestions for code structure, organization, and modularity. 
        4. **Testing and Validation:**
            - Outline the testing procedures and criteria for evaluating the program's success.
            - Define any specific test cases or scenarios that should be considered.
            - Specify the expected output or results for each test case. 

        **Note:**

        - Focus on clarity, conciseness, and completeness. Use technical terms and jargon appropriately for the intended audience.
        - Provide sufficient detail and examples to guide the programmer effectively.
        - Ensure that the assignment is well-structured and easy to follow.
    """
    analysis_response = model.generate_content(analysis_prompt, stream=True)
    analysis_response.resolve()
    time.sleep(20)

    add_to_log("Analysis", analysis_response.text)

    number_of_prog = 3

    teamlead_prompt = f"""
        You are a highly skilled and experienced team lead, known for your expertise in efficient task allocation and code optimization. You prioritize clarity, avoiding unnecessary duplication and complexity.

        **Technical Assignment:** 
        {analysis_response.text}

        **Your Task:**

        1. **Break Down the Assignment:** Carefully divide the technical assignment into {number_of_prog} distinct, equal-sized parts for {number_of_prog} Python developers. Each part should be well-defined and contribute meaningfully to the overall project. 
        2. **Allocate Tasks:** Distribute the {number_of_prog} parts to the developers, ensuring a balanced workload and avoiding overlapping responsibilities.
        3. **Code Organization:** For each programmer's tasks, divide the work into logical blocks, clearly separated by the markers "BLOCK_START" and "BLOCK_END". This will ensure clarity and simplify code integration later.

        **Additional Considerations:**

        - **Libraries & Frameworks:**  If specific libraries or frameworks are needed, recommend them to the programmers.
        - **Algorithm Choices:** If the task requires algorithms, suggest suitable ones and explain why they are appropriate.
        - **Code Style:**  Encourage programmers to write clean, readable code that adheres to PEP 8 style guidelines.

        **Example:**

        Programmer 1:
        BLOCK_START
        ... (technical specification for Programmer 1) ...
        BLOCK_END

        Programmer 2:
        BLOCK_START
        ... (technical specification for Programmer 2) ...
        BLOCK_END

        ... and so on for each programmer ...
    """

    teamlead_response = model.generate_content(teamlead_prompt, stream=True)
    teamlead_response.resolve()
    time.sleep(20)

    add_to_log("Teamlead", teamlead_response.text)

    # изначально хотел запоминать всю переписку
    development = ""

    tasks = extract_blocks(teamlead_response.text, "BLOCK_START", "BLOCK_END")

    # PYTHON DEVELOPERS
    programmers_responses = []
    programmers_code = []
    for count, task_ in enumerate(tasks):
        if count == 0:

            programmer_prompt = f"""
            You are a highly skilled and experienced senior multy-language developer, renowned for your ability to craft elegant and efficient solutions. You prioritize clarity, modularity, and maintainability in your code. 

            **Your Task:** {task_}

            **Guidelines:**

            - **Choose the Right Tools:** Select the most appropriate libraries and frameworks for the task, considering their strengths and suitability.  
            - **Minimize Complexity:**  Strive for a clean, straightforward solution, avoiding unnecessary complexity or redundancy. 
            - **Modular Design:** Break down your code into well-defined functions, classes, or modules to improve readability and maintainability.  
            - **Iterative Development:**  Implement your solution in a structured and iterative manner. Suggest small, testable steps that can be verified along the way.  

            **Output:**

            - **Code Format:**  Use a standard Python code block to present your solution.  
            - **Clear Comments:** Include concise and informative comments to explain the purpose of your code and any complex logic.
            - **Code Completion:** Write the entire code of the task, ensuring it is complete.
            - **Words with markers '&' are a mandatory part of the code**
            
            **Final Code Structure:**

            * Begin your code with the marker `&CODE_START`
            * End your code with the marker `&CODE_END`

            **Example:**

            ```python
            &CODE_START
            ... (code) ...
            &CODE_END
            ```
            
            OR
            
            ```html
            &CODE_START
            ... (code) ...
            &CODE_END
            ```
            
            """

        else:
            programmer_prompt = f"""
            You are a highly skilled and experienced senior multy-language developer, known for your ability to craft elegant and efficient solutions within a larger project context. You prioritize clarity, modularity, and maintainability in your code, ensuring seamless integration with existing code. 

            **Your Task:** {task_}

            **Context:** You're working on a large project, building upon the existing code provided below:

            ```python
            {development}
            ```

            **Guidelines:**

            - **Seamless Integration:** Ensure your code seamlessly integrates with the existing code, avoiding unnecessary duplication and complexity.
            - **Choose the Right Tools:** Select the most appropriate libraries and frameworks for the task, considering their strengths and suitability within the project.
            - **Modular Design:** Break down your code into well-defined functions, classes, or modules to improve readability and maintainability, ensuring consistent code style and structure.
            - **Iterative Development:** Implement your solution in a structured and iterative manner. Suggest small, testable steps that can be verified along the way to ensure smooth progress and avoid errors.
            - **Clear Explanations:** Include detailed comments explaining the logic behind your code, particularly when building upon existing code, making it easier to understand and maintain.
            - **Error Handling:** Implement robust error handling mechanisms to gracefully handle unexpected situations or user input.

            **Output:**

            - **Code Format:** Use a standard Python code block to present your solution.
            - **Code Completion:** Write the entire code solution, ensuring it is complete, ready to run, and seamlessly integrates with the provided code.
            - **Words with markers '&' are a mandatory part of the code**
            
            **Final Code Structure:**

            - Begin your code with the marker &CODE_START
            - End your code with the marker &CODE_END

            **Example:**

            ```python
            &CODE_START
            ... (code) ...
            &CODE_END
            ```
            
            OR
            
            ```html
            &CODE_START
            ... (code) ...
            &CODE_END
            ```
        """

        programmer_response = model.generate_content(programmer_prompt, stream=True)
        programmer_response.resolve()
        time.sleep(30)

        add_to_log("Programmer", programmer_response.text)

        code_of_programmer = extract_blocks(
            programmer_response.text, "&CODE_START", "&CODE_END"
        )[0]

        # Перепроверка
        errors = test_mistakes_with_gpt(programmer_response.text)
        add_to_log("debug", errors)

        programmer_debug_prompt = f"""
            You are a highly skilled and experienced senior multy-language developer, known for your ability to identify and fix bugs quickly and efficiently. You're a master of debugging and have a keen eye for detail. 

            **Your Task:**  You've been asked to review and fix the following Python code, which has some errors:

            ```
            {code_of_programmer}
            ```

            **What the code does:**
            {task_}

            **Error Log:**
            {errors}

            **Guidelines:**
            - **Analyze the Errors:** Carefully study the error messages provided. Understand the cause of each error and its potential impact on the code's functionality.
            - **Apply Fixes:** Implement precise and efficient fixes to correct the errors. Ensure that your changes address the root cause of the issue.
            - **Test Thoroughly:** After making corrections, test your code to confirm that the errors have been resolved and that the code functions as expected.
            - **Write code fully, completely without missing any code**
            **Output:**

            - **Code Format:** Use a standard Python code block to present your corrected code.
            - **Clear Comments:** Include comments to explain your fixes and any changes you've made to the original code.
            - **Words with markers '&' are a mandatory part of the code**
            
            **Final Code Structure:**

            - Begin your code with the marker &CODE_START
            - End your code with the marker &CODE_END
            markers are a mandatory part of the code
            "```python" , "```" are a mandatory part of the code
            **Example:**

            ```python
            &CODE_START
            ... (corrected code) ...
            &CODE_END
            ```
            
            OR
            
            ```html
            &CODE_START
            ... (corrected code) ...
            &CODE_END
            ```
            
        """
        programmer_response = model.generate_content(
            programmer_debug_prompt, stream=True
        )
        programmer_response.resolve()
        time.sleep(30)
        add_to_log("Programmer debuged", programmer_response.text)
        code_of_programmer = extract_blocks(
            programmer_response.text, "&CODE_START", "&CODE_END"
        )[0]
        development = evolution_of_development(development, code_of_programmer)

        programmers_responses.append(programmer_response.text)
        programmers_code.append(code_of_programmer)

    # все, что написали программисты
    programmers_responses_as_string = "\n\n".join(
        f"Programmer {i + 1}: \n{response}"
        for i, response in enumerate(programmers_responses)
    )

    # создать промпт который попишет нужные команды (прогеры уже напишут что нужно примерно делать)
    # в терминале для авто создания файлов для drf например через ls -R подать всё
    devops_req_terminal_prompt = f"""
    You are acting as a DevOps engineer responsible for setting up and maintaining the environment for a development project. Your primary task is to accurately create a `requirements.txt` file and determine the complete and correct set of terminal commands required to install and run a given framework or application. 
    **Project Overview:**

    - **Technical Assignment:** {analysis_response.text}
    - **Task Distribution:** {teamlead_response.text}
    - **Programmers' Code:** {programmers_responses_as_string}
    For example, if the project uses Django, you must ensure that the setup process is flawless. This includes creating a virtual environment, installing all the required dependencies from the `requirements.txt` file, initializing a new Django project, and setting up any necessary applications within the project.

    It is crucial that the terminal commands you choose are precise and error-free to ensure the project runs smoothly. You must consider any potential pitfalls, such as environment compatibility issues, dependency conflicts, or missing packages, and address these in your command sequence.

    Please write the `requirements.txt` file content between the markers `#FILE_REQ_START` and `#FILE_REQ_END`. Following that, list the full set of terminal commands needed for setting up the project between `#TERMINAL_START` and `#TERMINAL_END`. The commands should include steps for creating a virtual environment, installing dependencies, and any other necessary setup or configuration steps.

    #FILE_REQ_START
    ... code for requirements.txt ...
    #FILE_REQ_END

    #TERMINAL_START
    ... terminal commands ...
    #TERMINAL_END
    """
    devops_req_terminal_response = model.generate_content(
        devops_req_terminal_prompt, stream=True
    )
    devops_req_terminal_response.resolve()
    time.sleep(30)
    requirements = extract_blocks(
        devops_req_terminal_response.text, "#FILE_REQ_START", "#FILE_REQ_END"
    )

    add_to_log("Devops_req_terminal_response", devops_req_terminal_response.text)
    # понять куда сохранять req
    create_file(
        f"tests/{folder_obj.folder_name}",
        "requirements.txt",
        "\n".join(requirements),
    )

    terminal = extract_blocks(
        devops_req_terminal_response.text, "#TERMINAL_START", "#TERMINAL_END"
    )
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", terminal, "!!!!!!!!!!!")
    subprocess.run(
        f"cd tests\n cd {folder_obj.folder_name}" + "\n".join(terminal), shell=True
    )

    # DEVOPS
    devops_prompt = f"""
    You are a highly skilled and experienced DevOps engineer, known for your expertise in assembling complex projects from individual code contributions, ensuring seamless integration and functionality. You prioritize clarity, efficiency, and maintainability in your work.

    **Project Overview:**

    - **Technical Assignment:** {analysis_response.text}
    - **Task Distribution:** {teamlead_response.text}
    - **Programmers' Code:** {programmers_responses_as_string}

    **Your Task:**

    1. **Code Integration:** Assemble all the code written by the programmers into a single, working project, following the technical assignment.
    2. **Error Detection & Correction:**  Carefully identify and address any potential errors, inconsistencies, or missing code within the project.
    3. **Library Management:** Ensure that all necessary libraries are included and properly connected within the project. 
    4. **File Organization:**  Divide the project into well-structured files with appropriate names and extensions.  
    5. **File Linking:**  Implement import statements to link files correctly, ensuring that all necessary code is accessible within the project.
        - **Crucially, ensure that all necessary functions, classes, and variables are properly imported into the file with name `main` so that the project runs seamlessly.** 
    6. **Project Completion:**  Create a complete and functional project, ready for testing and deployment.
    7. **Package Listing:**  At the end, provide a list of all the packages used in the project, wrapped within the markers `&PACKAGES_START` and `&PACKAGES_END`.

    **Output Structure:**

    - **File Names:** Use the marker `NAME_START` to indicate the beginning of the file name and `NAME_END` to indicate the end.  
    - **File Content:**  Wrap each file's code within the markers `&FILE_START` and `&FILE_END`.
    - **Package List:**  Include the `&PACKAGES_START` and `&PACKAGES_END` markers followed by the space-separated list of package names at the end of the ouput
    - **Words with markers '&' are a mandatory part of the code**


    **Example:**

    NAME_START game.py NAME_END

    ```python
    &FILE_START
    ... code for game.py ...
    &FILE_END
    ```
    
    
    NAME_START index.html NAME_END
    
    ```html
    &FILE_START
    ... code for index.html ...
    &FILE_END
    ```
    

    ... other files ...

    NAME_START main.py NAME_END

    ```python
    &FILE_START
    ... code for main.py ...
    &FILE_END
    ```
    
    &PACKAGES_START
    pygame random etc...
    &PACKAGES_END
    
    """

    devops_response = model.generate_content(devops_prompt, stream=True)
    devops_response.resolve()
    time.sleep(20)

    codes = extract_blocks(devops_response.text, "&FILE_START", "&FILE_END")
    names = extract_blocks(devops_response.text, "NAME_START", "NAME_END")

    add_to_log("Devops", devops_response.text)

    files_as_string = "\n\n".join(
        f"**{name}**:\n{code}" for name, code in zip(names, codes)
    )

    errors = multyfile_test_mistakes_with_gpt(files_as_string)

    devops_debug_prompt = f"""
    You are a highly skilled and experienced DevOps engineer, known for your expertise in troubleshooting complex multi-file Python projects. You prioritize clarity, efficiency, and maintainability in your work.

    **Project Overview:**

    - **Technical Assignment:** {analysis_response.text}
    - **Task Distribution:** {teamlead_response.text}
    - **Programmers' Code:** {programmers_responses_as_string}
    - **Previous Code:** {files_as_string}
    - **Error Log:** {errors}
    - **Structure of project:** {get_ls_r_output(f"tests/{folder_obj.folder_name}")}

    **Your Task:**

    - **Identify the Root Cause:** Carefully analyze the error log and the previous code to pinpoint the root cause of the error.
    - **Implement Corrections:** Make the necessary changes to the code to fix the error. 
    - **Ensure Compatibility:** Ensure your corrections are compatible with the existing code, maintaining the functionality and integrity of the project. 
    - **Test Thoroughly:**  Thoroughly test your corrected code to ensure the error is resolved and the project works as expected.
    - **File Linking:**  Implement import statements to link files correctly, ensuring that all necessary code is accessible within the project.
    - **Crucially, ensure that all necessary functions, classes, and variables are properly imported into the `main` file so that the project runs seamlessly.** 
    In case of an error in the connection of the program files, rearrange everything so that it leads to correct operation
    **Output:**

    - **Corrected Code:** Provide the corrected version of the entire project code. Use the markers `&FILE_START` and `&FILE_END` to wrap each file's code.
    - **File Names:** Use the marker `NAME_START` to indicate the beginning of the file name and `NAME_END` to indicate the end. 
    - **Words with markers '&' are a mandatory part of the code**
    code blocks "```python" , "```" or "```html" , "```", etc...  are a mandatory part of the code
    - **Package List:**  Include the `&PACKAGES_START` and `&PACKAGES_END` markers followed by the space-separated list of package names at the end of the ouput

    **Example:**

    NAME_START game.py NAME_END

    ```python
    &FILE_START
    ... (corrected code for game.py) ...
    &FILE_END
    ```
    
    
    NAME_START index.html NAME_END
    
    ```html
    &FILE_START
    ... (corrected code for index.html) ...
    &FILE_END
    ```
    
    ... other files ...

    NAME_START main.py NAME_END

    ```python
    &FILE_START
    ... (corrected code for main.py) ...
    &FILE_END
    ```
    
    &PACKAGES_START
    pygame random time etc...
    &PACKAGES_END
    """

    # Если для решения ошибки потребуется работа с системой то для написания комманд в терминале используй кодовое слово "COMMAND" тут мб потребуется пошаговая система
    devops_response = model.generate_content(devops_debug_prompt, stream=True)
    devops_response.resolve()
    time.sleep(30)

    codes = extract_blocks(devops_response.text, "&FILE_START", "&FILE_END")
    names = extract_blocks(devops_response.text, "NAME_START", "NAME_END")

    files_as_string = "\n\n".join(
        f"**{name}**:\n{code}" for name, code in zip(names, codes)
    )

    packages_list = extract_blocks(
        devops_response.text, " &PACKAGES_START", "&PACKAGES_END"
    )

    sis_admin_prompt = f"""
        {packages_list}
        {files_as_string}
        {folder_obj.folder_name}
    """

    # import_list_of_packages(packages_list)

    create_file(
        f"tests/{folder_obj.folder_name}",
        "project_in_string_format.txt",
        devops_response.text,
    )
    add_to_log("Devops debuged", devops_response.text)
    # create_file(f"tests/{folder_obj.folder_name}", "__init__.py", devops_response.text)

    for name, code in zip(names, codes):
        create_file(f"tests/{folder_obj.folder_name}", f"{name}", code)

    try:
        # After creating all files, run pylint:
        pylint_results = run_pylint_with_ultimate_flags(
            [f"tests/{folder_obj.folder_name}/{name}" for name in names]
        )
        add_to_debug("Pylint", pylint_results)
    except Exception as e:
        add_to_debug("problem with pylint: ", e)
