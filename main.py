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
    alias_response = model.generate_content(f"output alias for task: {task_}. output only alias literally in few words",
                                            stream=True)  # Generate alias from task
    alias_response.resolve()
    return '_'.join(alias_response.text.split())


# уже писал, что не понимаю, работает ли ast.parse как запуск программы и поиск всех ошибок или только поиск синтаксических
def test_mistakes(code_string):
    errors = []
    try:
        _ = ast.parse(code_string)
        return None
    except Exception as e:
        error_message = traceback.format_exc()
        errors.append(error_message)
    return errors


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


def solve_task(task_):
    # technical writer

    analysis_prompt = f"""
        You are a professional technical writer of the big comprehensive project.
        Task: {task_}
        Conduct a technical analysis of this task.
        Write a technical assignment for the programmer.
        Describe all the principles of the program, libraries and algorithms.
    """
    analysis_response = model.generate_content(analysis_prompt, stream=True)
    analysis_response.resolve()
    print(analysis_response.text)

    add_to_log("Analysis", analysis_response.text)

    # изначально хотел запоминать всю переписку
    development = ''

    number_of_prog = 4

    teamlead_prompt = f"""
        You are a senior teamlead. 
        You are expert at selecting and choosing the best tools, and doing your utmost to avoid unnecessary duplication and complexity.
        technical assignment : {analysis_response.text}
        Conduct a technical analysis of this task.
        Write a technical assignment for the programmers.
        Describe all the principles of the program, libraries and algorithms.
        Break this technical assignment into {number_of_prog} parts for {number_of_prog} equal in volume work parts for {number_of_prog} python developers.
        Divide the tasks of each of the {number_of_prog} programmers into blocks, use the word "BLOCK_START" for start and "BLOCK_END" for end of each block.
        Distribute tasks so that everyone does something.
    """

    teamlead_response = model.generate_content(teamlead_prompt, stream=True)
    teamlead_response.resolve()
    print(teamlead_response.text)

    add_to_log("Teamlead", teamlead_response.text)

    tasks = extract_blocks(teamlead_response.text, "BLOCK_START", "BLOCK_END")
    # python developers
    programmers_responses = []
    programmers_code = []
    for count, task_ in enumerate(tasks):
        if count == 0:
            programmer_prompt = f"""
                You are a senior python developer.
                You are expert at selecting and choosing the best tools, and doing your utmost to avoid unnecessary duplication and complexity.
                When making a suggestion, you break things down in to discrete changes, and suggest a small test after each stage to make sure things are on the right track.
                Your problem will do its job in the best possible way.
                Write your code in python.
                The code should be output in the python code block.
                Your problem: {task_}

                Don't write any code except final version of your part.
                Finish writing the code to the end.
                Use code word "#CODE_START" for indication beginning and "#CODE_END" for ending of the final version of code
                Example:
                
                #CODE_START - note in the begining of code
                code ...
                #CODE_END - note in the end of code 
            """
        else:
            programmer_prompt = f"""
                You are a senior python developer.
                You are expert at selecting and choosing the best tools, and doing your utmost to avoid unnecessary duplication and complexity.
                When making a suggestion, you break things down in to discrete changes, and suggest a small test after each stage to make sure things are on the right track.
                Your problem will do its job in the best possible way.
                Write your code in python
                The code should be output in the python code block
                
                You're doing part of a big project. Do your task according to the code already written by other programmers
                The code already written before you: {development}. Do not repeat the code you have already written, but continue as it were.
                Your problem: {task_}

                Don't write any code except final version of your part.
                Finish writing the code to the end.
                Use code "#CODE_START" for indication beginning and "#CODE_END" for ending of the final version of your part of code
                Example:
                #CODE_START - note in the beginning of code
                code ...
                #CODE_END - note in the end of code 
            """

        programmer_response = model.generate_content(programmer_prompt, stream=True)
        programmer_response.resolve()
        time.sleep(4)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(programmer_response.text)
        add_to_log("Programmer", programmer_response.text)

        code_of_programmer = extract_blocks(programmer_response.text, "#CODE_START", "#CODE_END")[0]
        add_to_log("code", code_of_programmer)
        check = test_mistakes(code_of_programmer)

        while check is not None:
            programmer_debug_prompt = f"""
                You are a senior developer.
                Your problem will do its job in the best possible way.
                Write your code in python
                Leave brief comments when writing code.
                The code should be output in the python code block.
                You're doing part of a big project.
                
                Your problem: {task_}
                Your previous code: {code_of_programmer}
                Your traceback: {check}

                Fix the code according to the error log.
                Don't write any python code except the corrected version of your part.
                Use code "#CODE_START" for indication beginning and "#CODE_END" for ending of the corrected version of your part of code
                Example:
                
                #CODE_START - note in the beginning of code
                code ...
                #CODE_END - note in the end of code 
            """
            programmer_response = model.generate_content(programmer_debug_prompt, stream=True)
            programmer_response.resolve()
            code_of_programmer = extract_blocks(programmer_response.text, "#CODE_START", "#CODE_END")[0]
            check = test_mistakes(code_of_programmer)
            print("FFFFFFF")

        development = evolution_of_development(development, code_of_programmer)

        programmers_responses.append(programmer_response.text)
        programmers_code.append(code_of_programmer)
        print(programmer_response.text)

    programmers_responses_as_string = '\n\n'.join(
        f"Programmer {i + 1}: \n{response}"
        for i, response in enumerate(programmers_responses)
    )
    # programmers_code_as_string = '\n'.join(programmers_code)
    devops_prompt = f"""
        You are a senior devops.
        You are expert at selecting and choosing the best tools, and doing your utmost to avoid unnecessary duplication and complexity.
        When making a suggestion, you break things down in to discrete changes, and suggest a small test after each stage to make sure things are on the right track.
        technical assignment : {analysis_response.text}
        distribution of tasks : {teamlead_response.text}
        programmers responses: {programmers_responses_as_string}
        The code should be output in the python code block.
        Assemble all the code written by programmers into one full-fledged, working project, according to the technical assignment, look for possible mistakes, defections, losses of code and fix them.
        If necessary, add everything you need.
        And the distribution of tasks will help you figure it out.
        Don't forget to connect all the libraries you use.
        
        Divide the project into files in the best possible way, do not forget to link files together with importation.
        Perform all the necessary code manipulations that are needed to link the file into one project
        
        Come up with a name for each file and don't forget to set their extension. Before the code use the word "NAME_START" for indication beginning and "NAME_END" for ending of each name. the main file should be called "main.py", write it before the code of the file
        Use code word "#FILE_START" for indication beginning and "#FILE_END" for ending of each file. 
        Example:
        
        NAME_START game.py NAME_END
        
        #FILE_START - note in the beginning of code
        code ...
        #FILE_END - note in the end of code
        

        Finally, create a list of the names of the packages used in the code. Before output, use the code word "#PACKAGES" as a separator there will be spaces. Write code word and list in one string. leave this string at the end of the main file.
    """
    devops_response = model.generate_content(devops_prompt, stream=True)
    devops_response.resolve()

    codes = extract_blocks(devops_response.text, "#FILE_START", "#FILE_END")
    names = extract_blocks(devops_response.text, "NAME_START", "NAME_END")

    # devops_debug_prompt_without_traceback = f"""
    #         You are a senior devops.
    #         technical assignment : {analysis_response.text}
    #         distribution of tasks : {teamlead_response.text}
    #         programmers responses: {programmers_responses_as_string}
    #         Your previous code: {answer}
    #         Your traceback: {check}
    #
    #         Fix the code according to the error log.
    #         As an answer write only the corrected version of code
    #     """

    # check = test_mistakes(answer)
    #
    # # надеюсь тут возникнут проблемы тк тогда это будет значить, что ошибки не только синтаксические и для их починки потребуется доступ к файлам и картинкам
    # while check is not None:
    #     devops_debug_prompt = f"""
    #         You are a senior devops.
    #         technical assignment : {analysis_response.text}
    #         distribution of tasks : {teamlead_response.text}
    #         programmers responses: {programmers_responses_as_string}
    #         Your previous code: {answer}
    #         Your traceback: {check}
    #
    #         Fix the code according to the error log.
    #         As an answer write only the corrected version of code
    #     """
    #     # Если для решения ошибки потребуется работа с системой то для написания комманд в терминале используй кодовое слово "COMMAND" тут мб потребуется пошаговая система
    #     devops_response = model.generate_content(devops_debug_prompt, stream=True)
    #     devops_response.resolve()
    #     answer = devops_response.text.split("`python")[-1].split("```")[0]
    #     check = test_mistakes(answer)
    #     print(check)

    # packages_list = devops_response.text.split("PACKAGES")[1].split(' ')
    # import_list_of_packages(packages_list)
    print(devops_response.text)
    add_to_log("Devops", devops_response.text)

    for name, code in zip(names, codes):
        create_file(f"tests/{folder_name}", f"{name}", code)


task = input("Введите задачу: ")
folder_name = generate_alias(task)  # название папки, в которую все сохранится
file_work(task, folder_name)

solve_task(task)

print("FINITA")

# TESTS
# Напиши приложение архиватор с графическим интерфейсом на языке python. Алгоритм архивации реализуй самостоятельно
# task = "write me a classic game of life in pygame"
