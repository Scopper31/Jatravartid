# -*- coding: utf-8 -*-
# pip install google-generativeai
# from alive_progress import alive_bar
#qdaWDdaw
#adwadawd
from solve import *
from utilities import *
from config import *
from correction import *


def main():
    # try:
    #     ask = int(input("Новый проект: 1, Ввести коррекцию в старый 2: "))
    # except ValueError:
    #     print("Ошибка: введено не число. Попробуйте снова.")
    #     return
    #     # try:
    # if ask == 1:
    task = input("Введите задачу: ")

    # with alive_bar(100, title="Обработка данных") as bar:
    #    pass
    def bar():
        pass

    set_folder_name(
        generate_alias(task, bar)
    )  # название папки, в которую все сохранится
    print("Folder name: ", folder_obj.folder_name)
    file_work(task)
    solve_task(task, bar)
    print("FINITA")
    # else:
    #     set_folder_name(input("Название проекта: "))
    #     while True:
    #         task = input("Правка: ")
    #         develop(task, bar)
    # except Exception as e:
    #     print(f"Произошла ошибка: {e}")
    #     add_to_log("Main", e)


if __name__ == "__main__":
    main()


# TESTS
# Напиши приложение архиватор с графическим интерфейсом на языке python. Алгоритм архивации реализуй самостоятельно
# task = "write me a classic game of life in pygame"
