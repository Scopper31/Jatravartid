import time
from config import model
from pylint.lint import Run
from pylint.reporters.text import TextReporter
import io
from utilities.system_utilities import add_to_log


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
    try:
        debug_response = model.generate_content(debug_prompt, stream=True)
        debug_response.resolve()
    except Exception as e:
        print(f"Error in generating or resolving content: {e}")
        add_to_log("GPT Debug", e)
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

        **Connection Errors:** The error lies in the incorrect linking of files. (We need to get rid of the mutual connection of files. And make a working set of files.)
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
    try:
        debug_response = model.generate_content(debug_prompt, stream=True)
        debug_response.resolve()
    except Exception as e:
        print(f"Error in generating or resolving content for multi-file: {e}")
        add_to_log("GPT Multi-file Debug", e)
    time.sleep(20)
    return debug_response.text


def run_pylint_with_ultimate_flags(files_to_lint):
    pylint_output = io.StringIO()  # Custom open stream for pylint output
    reporter = TextReporter(pylint_output)

    # Define your ultimate set of flags here!
    # For example, to enable all checks except for line-too-long:
    pylint_arguments = [
        "--disable=all",
        "--enable=similarities,classes,design,exceptions,format,imports,logging,method_args,miscellaneous,refactoring,spelling,string,typecheck,variables,broad_try_clause,code_style,deprecated_builtins,dunder,magic-value,parameter_documentation,typing",
        "--disable=line-too-long",  # Example: disable line-too-long check
    ] + files_to_lint
    try:
        Run(pylint_arguments, reporter=reporter, exit=False)
    except Exception as e:
        print(f"Error running pylint: {e}")
        add_to_log("Pylint", e)

    return pylint_output.getvalue()
