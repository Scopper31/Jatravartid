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

API_KEY = ""
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')


def import_list_of_packages(packages):
    for package in packages:
        pip.main(['install', package])


def evolution_of_development(a, b):
    return '\n'.join([a, b])


def file_work(task, alias):
    try:
        os.makedirs(f"tests/{alias}", exist_ok=True)  # Create folder in "tests"

        with open(f"tests/{alias}/log.txt", "a") as log_file:
            log_file.write(f"\n--- {datetime.datetime.now()} ---\n")
            log_file.write(f"Task: {task}\n")
            log_file.write("=" * 50 + "\n\n")
    except FileNotFoundError:
        print(f"Файл не найден, произошла ошибка.")

def create_file(code, name, path):
    with open(f"{path}/{name}.py", "w") as file:
        file.write(code)

def generate_alias(task):
    alias_response = model.generate_content(f"output alias for task: {task}. output only alias", stream=True)  # Generate alias from task
    alias_response.resolve()
    time.sleep(4)
    return '_'.join((alias_response.text).split())

def test_mistakes(code_string):
    errors = []
    try:
        _ = ast.parse(code_string)
        return None
    except Exception as e:
        error_message = traceback.format_exc()
        errors.append(error_message)
    return errors


def solve_task(problem):
    # technical writer

    analysis_prompt = f"""
        You are a professional technical writer of the big comprehensive project.
        Task: {problem}
        Conduct a technical analysis of this task.
        Write a technical assignment for the programmer.
        Describe all the principles of the program, libraries and algorithms.
    """
    analysis_response = model.generate_content(analysis_prompt, stream=True)
    analysis_response.resolve()
    print(analysis_response.text)

    with open(f"tests/{alias}/log.txt", "a") as log_file:
        log_file.write(f"Analysis:\n{analysis_response.text}\n")

    # development = evolution_of_development(development, response.text)

    teamlead_prompt = f"""
        You are a senior teamlead.
        technical assignment : {analysis_response.text}
        Conduct a technical analysis of this task.
        Write a technical assignment for the programmers.
        Break this technical assignment into 4 parts for 4 parts for 4 python developers.
        Divide the tasks of each of the 4 programmers into blocks, use the word "BLOCK" for start of each block.
        Describe all the principles of the program, libraries and algorithms.
    """

    teamlead_response = model.generate_content(teamlead_prompt, stream=True)
    teamlead_response.resolve()
    print(teamlead_response.text)
    with open(f"tests/{alias}/log.txt", "a") as log_file:
        log_file.write(f"Teamlead:\n{teamlead_response.text}\n")

    tasks = teamlead_response.text.split("BLOCK")[1:]

    # python developers
    programmers_responses = []
    programmers_code = []
    for problem in tasks:
        programmer_prompt = f"""
            You are a senior developer.
            Your problem will do its job in the best possible way.
            Write your code in python
            Leave brief comments when writing code.
            Your problem: {problem}
        """

        programmer_response = model.generate_content(programmer_prompt, stream=True)
        programmer_response.resolve()

        code_of_programmer = programmer_response.text.split("`python")[1].split("```")[0]
        check = test_mistakes(code_of_programmer)

        while check is not None:
            programmer_debug_prompt = f"""
                You are a senior developer.
                Your problem will do its job in the best possible way.
                Write your code in python
                Leave brief comments when writing code.
                Your problem: {problem}
                Your previous code: {code_of_programmer}
                Your traceback: {check}

                Fix the code according to the error log.
                Don't write any more python code except the corrected version.
            """
            programmer_response = model.generate_content(programmer_debug_prompt, stream=True)
            programmer_response.resolve()
            code_of_programmer = programmer_response.text.split("`python")[1].split("```")[0]
            check = test_mistakes(code_of_programmer)

        programmers_responses.append(programmer_response.text)
        programmers_code.append(code_of_programmer)
        print(programmer_response.text)
        with open(f"tests/{alias}/log.txt", "a") as log_file:
            log_file.write(f"Programmer:\n{programmer_response.text}\n")

    programmers_responses_as_string = '\n'.join(programmers_responses)
    # programmers_code_as_string = '\n'.join(programmers_code)
    devops_prompt = f"""
        You are a senior devops.
        technical assignment : {analysis_response.text}
        distribution of tasks : {teamlead_response.text}
        programmers responses: {programmers_responses_as_string}
        Assemble all the code written by programmers into one full-fledged, working project, according to the technical assignment, look for possible mistakes and fix them
        And the distribution of tasks will help you figure it out.

        Finally, create a list of the names of the packages used in the code. Before output, use the code word "#PACKAGES" as a separator there will be spaces
    """
    devops_response = model.generate_content(devops_prompt, stream=True)
    devops_response.resolve()
    answer = devops_response.text.split("`python")[1].split("```")[0]
    # packages_list = devops_response.text.split("PACKAGES")[1].split(' ')
    # import_list_of_packages(packages_list)
    print(devops_response.text)
    with open(f"tests/{alias}/log.txt", "a") as log_file:
        log_file.write(f"Devops:\n{devops_response.text}\n")
    return answer


task = input("Введите задачу: ")
# task = "write me a classic game of life in pygame"

alias = generate_alias(task)
file_work(task, alias)

final_result = solve_task(task)
final_result = f"#{task}\n\n{final_result}"

create_file(final_result, "script", f"tests/{alias}")

print("FINITA")