from utilities import *


def main(path_to_project, question, gemiAI=True):
    analysis_response = analisys_of_project(path_to_project, question, gemiAI)
    with open(f"small_app_folder/info.txt", "w") as f:
        f.write(analysis_response)
    return analysis_response


if __name__ == "__main__":
    path_to_project = "/Users/sergeybudygin/Desktop/AirLiquid/AL/parsing"
    question = "мне нужно чтобы в бота отправлялось сл васех сайтов как это сделать?"

    print(main(path_to_project, question, False))
