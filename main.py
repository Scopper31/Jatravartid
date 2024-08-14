# -*- coding: utf-8 -*-
# pip install google-generativeai
from solve import *
from utilities.neuro_utilities import *
from config import *
from correction import *


def main():
    ask = int(input("Новый проект: 1, Ввести коррекцию в старый 2: "))
    if ask == 1:
        task = input("Введите задачу: ")
        set_folder_name(generate_alias(task))  # название папки, в которую все сохранится
        print(folder_obj.folder_name)
        file_work(task)
        solve_task(task)

        print("FINITA")

    else:
        set_folder_name(input("Название проекта: "))

        while 1:
            task = input("Правка: ")
            develop(task)


if __name__ == "__main__":
    main()

# TESTS
# Напиши приложение архиватор с графическим интерфейсом на языке python. Алгоритм архивации реализуй самостоятельно
# task = "write me a classic game of life in pygame"