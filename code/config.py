import google.generativeai as genai
import os

# gemini конфигурация
# API_KEY = "AIzaSyDLHHsHyTOHOUkErElPpnvbPsJ7dcu2BKc" #alex
API_KEY = "AIzaSyBM6bOXdvcdacg-Bo9SavNY7WqTnqI4Zzw" #svb
"AIzaSyCOtj2v7Thm2GH7liup-wH_35OgmNAg2jU" # М
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


# variables
class Folder_Name:
    def __init__(self):
        self.folder_name = ""


folder_obj = Folder_Name()


def set_folder_name(new_name, *args, **kwargs):
    global folder_obj
    folder_obj.folder_name = new_name
    os.makedirs(f"tests/{new_name}", exist_ok=True)
