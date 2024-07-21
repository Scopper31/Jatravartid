# pip install google-generativeai
import os
import time
import google.generativeai as genai
# from google.generativeai import caching
import io
import datetime
import re
import pip
import ast
import traceback


# gemini конфигурация
API_KEY = "AIzaSyDDc_34aQhK3sikAgQJqXsvxyRmGsxKdfQ"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')


# эту функцию надо вставлять в самое начало сгенерированного кода вместе с массивом packages
def import_list_of_packages(packages):
    for package in packages:
        pip.main(['install', package])


def evolution_of_development(a, b):
    return '\nA piece of code:\n'.join([a, b])


# создание папки с проектом и объявление лога
def file_work(task_, folder_name):
    try:
        os.makedirs(f"tests/{folder_name}", exist_ok=True)  # Create folder in "tests"

        with open(f"tests/{folder_name}/log.txt", "a") as log_file:
            log_file.write(f"\n--- {datetime.datetime.now()} ---\n")
            log_file.write(f"Task: {task_}\n")
            log_file.write("=" * 50 + "\n\n")
    except FileNotFoundError:
        print(f"Файл не найден, произошла ошибка.")


def create_file(path_to_folder, name, code):
    with open(f"{path_to_folder}/{name}", "w") as file:
        file.write(code)


# под вопросом. тк возможно создание двух одинаковый файлов или переполнение длинны названия (221 символ)
def generate_alias(task_):
    alias_response = model.generate_content(f"output alias for task, that will be the name of folder with the project: {task_}. output only alias literally in few words without wrapping in \"**\"",
                                            stream=True)  # Generate alias from task
    alias_response.resolve()
    return '_'.join(alias_response.text.split())


def test_mistakes_with_gpt(code_string):
    debug_prompt = f"""
        You are a highly skilled Python debugger with a keen eye for detail. You are tasked with meticulously reviewing the following Python code snippet and identifying all potential errors. 
        
        **Code**
        
        ```python
        {code_string}
        ```
        
        Your goal is to find as many errors as possible, including but not limited to:
        
        * Syntax Errors:  Missing parentheses, commas, incorrect indentation, invalid keywords, typos, misplaced operators, etc.
        * Runtime Errors: Errors that occur during code execution (e.g., division by zero, accessing non-existent variables, incorrect indexing, type mismatches, etc.)
        * Logical Errors:  Incorrect logic that leads to unexpected results, infinite loops, unintended side effects, incorrect variable usage, etc.
        * Style Violations: Code that doesn't adhere to PEP 8 style guidelines (e.g., inconsistent naming conventions, excessive line length, inappropriate spacing, etc.)
        * Potential Bugs:  Flaws in the code that could lead to unexpected behavior, security vulnerabilities, or performance issues, including but not limited to:
            - Incorrect handling of edge cases
            - Unintentional data corruption
            - Lack of proper input validation
            - Race conditions in multi-threaded scenarios
            - Unnecessary complexity or inefficient algorithms 
        
        For each error you identify, provide a detailed explanation, including:
        
        1. Line Number:  The specific line where the error occurs.
        2. Error Type: A concise description of the error (e.g., SyntaxError, TypeError, ValueError, Logical Error, Style Violation, Potential Bug, etc.).
        3. Explanation:  A clear and detailed description of why the error occurs. Provide context and reasoning, and explain how the error could impact the code's functionality or security.
        4. Suggested Fix:  Provide a specific recommendation on how to fix the error and ensure the code behaves correctly, securely, and efficiently.
        
        markers of beginning and ending of something are a mandatory part of the code
        "```python" , "```" are a mandatory part of the code
    """
    debug_response = model.generate_content(debug_prompt, stream=True)
    debug_response.resolve()
    time.sleep(10)
    return debug_response.text


def multyfile_test_mistakes_with_gpt(code_string):
    debug_prompt = f"""
    You are a highly skilled Python debugger with a keen eye for detail. You are tasked with meticulously reviewing the following multi-file Python project and identifying all potential errors. 

    **Project Structure:**

    **File 1: file1_name.py**

    ```python
    file1_code
    ```
    
    **File 2: file2_name.py**
    
    ```python
    file1_code
    ```

    ... (Additional files if needed) ...
    
    **Your Goal:**
    
    Your goal is to find as many errors as possible, including but not limited to:
    
    **Syntax Errors:** Missing parentheses, commas, incorrect indentation, invalid keywords, typos, misplaced operators, etc.
    **Runtime Errors:** Errors that occur during code execution (e.g., division by zero, accessing non-existent variables, incorrect indexing, type mismatches, etc.)
    **Logical Errors:** Incorrect logic that leads to unexpected results, infinite loops, unintended side effects, incorrect variable usage, etc.
    **Style Violations:** Code that doesn't adhere to PEP 8 style guidelines (e.g., inconsistent naming conventions, excessive line length, inappropriate spacing, etc.)
    **Potential Bugs:** Flaws in the code that could lead to unexpected behavior, security vulnerabilities, or performance issues, including but not limited to:
        - Incorrect handling of edge cases
        - Unintentional data corruption
        - Lack of proper input validation
        - Race conditions in multi-threaded scenarios
        - Unnecessary complexity or inefficient algorithms
    **Code Connectivity Issues:** Identify any problems with how files are imported or referenced, leading to missing modules, undefined variables, or incorrect function calls across files.
    
    **For each error you identify, provide a detailed explanation, including:**
    
    **File Name:** The name of the file where the error occurs.
    **Line Number:** The specific line where the error occurs.
    **Error Type:** A concise description of the error (e.g., SyntaxError, TypeError, ValueError, Logical Error, Style Violation, Potential Bug, Import Error, etc.).
    **Explanation:** A clear and detailed description of why the error occurs. Provide context and reasoning, and explain how the error could impact the code's functionality or security.
    **Suggested Fix:** Provide a specific recommendation on how to fix the error and ensure the code behaves correctly, securely, and efficiently.
    
    
    markers of beginning and ending of something are a mandatory part of the code
    "```python" , "```" are a mandatory part of the code
    
    **Example:**
    
    File: my_module.py
    Error on line 10: NameError: name 'my_variable' is not defined
    Explanation: The variable my_variable is used in this file, but it's not defined within this file or imported from another file.
    Suggested Fix: Either define my_variable in this file or import it from the file where it is defined.
    Important: Be thorough in your analysis, and aim to find as many errors as possible. Explain your reasoning clearly and provide specific recommendations for fixes. Don't hesitate to identify potential bugs, even if they are not immediately apparent during a quick glance.
    """
    debug_response = model.generate_content(debug_prompt, stream=True)
    debug_response.resolve()
    time.sleep(20)
    return debug_response.text


def add_to_log(worker_type, response):
    with open(f"tests/{folder_name}/log.txt", "a") as log_file:
        log_file.write(f"{worker_type}:\n{response}\n")


def extract_blocks(text, block_start, block_end):
    block_starts = [m.start() for m in re.finditer(block_start, text)]
    block_ends = [m.start() for m in re.finditer(block_end, text)]

    extracted_texts = []
    for start, end in zip(block_starts, block_ends):
        extracted_texts.append(text[start + len(block_start):end].strip())

    return extracted_texts


def develop(task_, folder_name_):
    with open(f"""tests/{folder_name_}/project_in_string_format.txt""") as file:
        code = file.read()

    prompt = f"""
    Please help me fix the following Python project. I want to make the following changes:

    {task_}

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
        with open(f"tests/{folder_name_}number.txt", "r") as file:
            number = int(file.read())
        number += 1
        with open(f"tests/{folder_name_}number.txt", "w") as file:
            file.write(str(number))
    except FileNotFoundError:
        with open(f"tests/{folder_name_}number.txt", "w") as file:
            file.write("0")
            number = 0
    for name, code in zip(names, codes):
        create_file(f"tests/{folder_name_}/correction{number}", f"{name}", code)
    time.sleep(20)


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
    print(analysis_response.text)

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
    print(teamlead_response.text)

    add_to_log("Teamlead", teamlead_response.text)

    # изначально хотел запоминать всю переписку
    development = ''

    tasks = extract_blocks(teamlead_response.text, "BLOCK_START", "BLOCK_END")

    # PYTHON DEVELOPERS
    programmers_responses = []
    programmers_code = []
    for count, task_ in enumerate(tasks):
        if count == 0:

            programmer_prompt = f"""
            You are a highly skilled and experienced senior Python developer, renowned for your ability to craft elegant and efficient solutions. You prioritize clarity, modularity, and maintainability in your code. 

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

            **Final Code Structure:**

            * Begin your code with the marker `#CODE_START`
            * End your code with the marker `#CODE_END`

            **Example:**

            ```python
            #CODE_START
            ... (code) ...
            #CODE_END
            ```
            """

        else:
            programmer_prompt = f"""
            You are a highly skilled and experienced senior Python developer, known for your ability to craft elegant and efficient solutions within a larger project context. You prioritize clarity, modularity, and maintainability in your code, ensuring seamless integration with existing code. 

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
            
            **Final Code Structure:**
            
            - Begin your code with the marker #CODE_START
            - End your code with the marker #CODE_END
            
            **Example:**
            
            ```python
            #CODE_START
            ... (code) ...
            #CODE_END
            ```
        """

        programmer_response = model.generate_content(programmer_prompt, stream=True)
        programmer_response.resolve()
        time.sleep(10)
        print("=============================================================================================================================================")
        print(programmer_response.text)
        add_to_log("Programmer", programmer_response.text)

        code_of_programmer = extract_blocks(programmer_response.text, "#CODE_START", "#CODE_END")[0]

        #Перепроверка
        errors = test_mistakes_with_gpt(programmer_response.text)
        add_to_log("debug", errors)
        print(errors)

        programmer_debug_prompt = f"""
            You are a highly skilled and experienced senior Python developer, known for your ability to identify and fix bugs quickly and efficiently. You're a master of debugging and have a keen eye for detail. 

            **Your Task:**  You've been asked to review and fix the following Python code, which has some errors:
            
            ```python
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
            
            **Output:**
            
            - **Code Format:** Use a standard Python code block to present your corrected code.
            - **Clear Comments:** Include comments to explain your fixes and any changes you've made to the original code.
            
            **Final Code Structure:**
            
            - Begin your code with the marker #CODE_START
            - End your code with the marker #CODE_END
            markers are a mandatory part of the code
            "```python" , "```" are a mandatory part of the code
            **Example:**
            
            ```python
            #CODE_START
            ... (corrected code) ...
            #CODE_END
            ```
        """
        programmer_response = model.generate_content(programmer_debug_prompt, stream=True)
        programmer_response.resolve()
        time.sleep(20)
        code_of_programmer = extract_blocks(programmer_response.text, "#CODE_START", "#CODE_END")[0]
        add_to_log("Programmer debuged", programmer_response.text)
        development = evolution_of_development(development, code_of_programmer)

        programmers_responses.append(programmer_response.text)
        programmers_code.append(code_of_programmer)

    #все, что написали программисты
    programmers_responses_as_string = '\n\n'.join(
        f"Programmer {i + 1}: \n{response}"
        for i, response in enumerate(programmers_responses)
    )

    #DEVOPS
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
        - **Crucially, ensure that all necessary functions, classes, and variables are properly imported into the `main.py` file so that the project runs seamlessly.** 
    6. **Project Completion:**  Create a complete and functional project, ready for testing and deployment.
    7. **Package Listing:**  Provide a list of all the packages used in the project, separated by the marker `#PACKAGES`. Include this list at the end of the main file.

    **Output Structure:**

    - **File Names:** Use the marker `NAME_START` to indicate the beginning of the file name and `NAME_END` to indicate the end.  
    - **File Content:**  Wrap each file's code within the markers `#FILE_START` and `#FILE_END`.
    - **Package List:**  Include the `#PACKAGES` marker followed by the space-separated list of package names at the end of the main file (`main.py`).
    markers are a mandatory part of the code

    **Example:**
    
    NAME_START game.py NAME_END
    
    ```python
    #FILE_START
    ... code for game.py ...
    #FILE_END
    ```
    
    ... other files ...

    NAME_START main.py NAME_END
    
    ```python
    #FILE_START
    ... code for main.py ...
    #PACKAGES pygame random
    #FILE_END
    ```
    """

    devops_response = model.generate_content(devops_prompt, stream=True)
    devops_response.resolve()
    time.sleep(20)

    codes = extract_blocks(devops_response.text, "#FILE_START", "#FILE_END")
    names = extract_blocks(devops_response.text, "NAME_START", "NAME_END")

    add_to_log("Devops", devops_response.text)

    files_as_string = '\n\n'.join(
        f"<{name}>:\n{code}"
        for name, code in zip(names, codes)
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

    **Your Task:**

    - **Identify the Root Cause:** Carefully analyze the error log and the previous code to pinpoint the root cause of the error.
    - **Implement Corrections:** Make the necessary changes to the code to fix the error. 
    - **Ensure Compatibility:** Ensure your corrections are compatible with the existing code, maintaining the functionality and integrity of the project. 
    - **Test Thoroughly:**  Thoroughly test your corrected code to ensure the error is resolved and the project works as expected.
    - **File Linking:**  Implement import statements to link files correctly, ensuring that all necessary code is accessible within the project.
    make snake game but portals of different color appear over time that snake can teleport through- **Crucially, ensure that all necessary functions, classes, and variables are properly imported into the `main.py` file so that the project runs seamlessly.** 
     
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

    # Если для решения ошибки потребуется работа с системой то для написания комманд в терминале используй кодовое слово "COMMAND" тут мб потребуется пошаговая система
    devops_response = model.generate_content(devops_debug_prompt, stream=True)
    devops_response.resolve()
    time.sleep(20)

    codes = extract_blocks(devops_response.text, "#FILE_START", "#FILE_END")
    names = extract_blocks(devops_response.text, "NAME_START", "NAME_END")


    # packages_list = devops_response.text.split("PACKAGES")[1].split(' ')
    # import_list_of_packages(packages_list)

    print(devops_response.text)
    create_file(f"tests/{folder_name}", "project_in_string_format.txt", devops_response.text)
    add_to_log("Devops debuged", devops_response.text)

    for name, code in zip(names, codes):
        create_file(f"tests/{folder_name}", f"{name}", code)

ask = int(input("Новый проект: 1, Ввести коррекцию в старый 2: "))
if ask == 1:
    task = input("Введите задачу: ")
    folder_name = generate_alias(task)  # название папки, в которую все сохранится
    file_work(task, folder_name)

    solve_task(task)

    print("FINITA")

else:
    folder_name = input("Название проекта: ")

    while 1:
        task = input("Правка: ")
        develop(task, folder_name)


# TESTS
# Напиши приложение архиватор с графическим интерфейсом на языке python. Алгоритм архивации реализуй самостоятельно
# task = "write me a classic game of life in pygame"
