import os
import subprocess
import sys
import datetime
from config import folder_obj


def execute_command(command):
    try:
        project_path = os.path.dirname(sys.argv[0])
        # Переходим в папку проекта
        os.chdir(project_path)

        # Выполняем команду
        result = subprocess.run(command.split(), capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Выполнение команды: {command}")
            print(f"Вывод: {result.stdout}")
        else:
            print(f"Ошибка выполнения команды: {command}")
            print(f"Ошибка: {result.stderr}")

        # Возвращаемся в исходную папку
        os.chdir(os.path.dirname(project_path))  # Возвращаемся в родительскую папку

    except FileNotFoundError:
        print(f"Команда не найдена: {command}")
    except Exception as e:
        print(f"Ошибка при выполнении команды: {e}")


# создание папки с проектом и объявление лога
def file_work(task, *args, **kwargs):
    try:
        os.makedirs(
            f"tests/{folder_obj.folder_name}", exist_ok=True
        )  # Create folder in "tests"

        with open(f"tests/{folder_obj.folder_name}/debug.txt", "a") as log_file:
            log_file.write(f"\n--- {datetime.datetime.now()} ---\n")
            log_file.write(f"Task: {task}\n")
            log_file.write("=" * 50 + "\n\n")

        with open(f"tests/{folder_obj.folder_name}/log.txt", "a") as log_file:
            log_file.write(f"\n--- {datetime.datetime.now()} ---\n")
            log_file.write(f"Task: {task}\n")
            log_file.write("=" * 50 + "\n\n")
    except FileNotFoundError:
        print(f"Файл не найден, произошла ошибка.")


def create_file(path_to_folder, name, code):
    try:
        with open(f"{path_to_folder}/{name}", "w") as file:
            file.write(code)
    except OSError as e:
        print(f"Failed to create or write to file {name} in {path_to_folder}: {e}")
        add_to_log("create_file", e)

    except Exception as e:
        print(f"Unexpected error while creating file {name}: {e}")
        add_to_log("create_file", e)


def add_to_log(worker_type, response):
    try:
        with open(f"tests/{folder_obj.folder_name}/log.txt", "a") as log_file:
            log_file.write(f"{worker_type}:\n{response}\n")
    except OSError as e:
        print(f"Failed to write to log file: {e}")
    except Exception as e:
        print(f"Unexpected error while logging: {e}")


def add_to_process(worker_type, response):
    try:
        with open(f"tests/{folder_obj.folder_name}/process.txt", "a") as log_file:
            log_file.write(f"{worker_type}:\n{response}\n")
    except OSError as e:
        print(f"Failed to write to log file: {e}")
    except Exception as e:
        print(f"Unexpected error while logging: {e}")


def add_to_debug(worker_type, response):
    try:
        with open(f"tests/{folder_obj.folder_name}/debug.txt", "a") as debug_file:
            debug_file.write(f"{worker_type}:\n{response}\n")
    except OSError as e:
        print(f"Failed to write to debug file: {e}")
    except Exception as e:
        print(f"Unexpected error while debugging: {e}")
