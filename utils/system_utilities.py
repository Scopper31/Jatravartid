import os
import subprocess
import sys
import datetime
from config import folder_name

def execute_command(command):
    try:
        project_path = os.path.dirname(sys.argv[0])
        # Переходим в папку проекта
        os.chdir(project_path)

        # Выполняем команду
        result = subprocess.run(command.split(), capture_output=True, text=True)
        if result.returncode == 0:
            print(f'Выполнение команды: {command}')
            print(f'Вывод: {result.stdout}')
        else:
            print(f'Ошибка выполнения команды: {command}')
            print(f'Ошибка: {result.stderr}')

        # Возвращаемся в исходную папку
        os.chdir(os.path.dirname(project_path))  # Возвращаемся в родительскую папку

    except FileNotFoundError:
        print(f'Команда не найдена: {command}')
    except Exception as e:
        print(f"Ошибка при выполнении команды: {e}")


# создание папки с проектом и объявление лога
def file_work(task):
    try:
        os.makedirs(f"tests/{folder_name}", exist_ok=True)  # Create folder in "tests"

        with open(f"tests/{folder_name}/log.txt", "a") as log_file:
            log_file.write(f"\n--- {datetime.datetime.now()} ---\n")
            log_file.write(f"Task: {task}\n")
            log_file.write("=" * 50 + "\n\n")
    except FileNotFoundError:
        print(f"Файл не найден, произошла ошибка.")


def create_file(path_to_folder, name, code):
    with open(f"{path_to_folder}/{name}", "w") as file:
        file.write(code)


def add_to_log(worker_type, response):
    with open(f"tests/{folder_name}/log.txt", "a") as log_file:
        log_file.write(f"{worker_type}:\n{response}\n")