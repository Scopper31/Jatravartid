import os
import subprocess


def list_directory_recursive_to_string(directory):
    """аналог ls -R возможно не работает"""
    result = []

    for root, dirs, files in os.walk(directory):
        result.append(f"{root}:\n")
        for file in files:
            result.append(f"  {file}\n")
        for dir in dirs:
            result.append(f"  {dir}/\n")
        result.append("\n")

    return "".join(result)


def get_ls_r_output(path):
    """
    Функция, которая возвращает вывод команды `ls -R` для заданного пути в виде строки.
    """
    result = subprocess.run(["ls", "-R", path], capture_output=True, text=True)
    return result.stdout
