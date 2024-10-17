import google.generativeai as genai
import os
import random
from dotenv import load_dotenv
load_dotenv()
   
api_keys = []
try:
    for key, value in os.environ.items():
        if key.startswith("API_GEMIAI_KEY"):
            api_keys.append(value)

    genai.configure(api_key=random.choice(api_keys))
except IndexError as e:
    print("Error with API keys:", e)
    exit(1)
model_pro, model_flash = "gemini-pro", "gemini-1.5-flash"
model = genai.GenerativeModel(model_pro)


# variables
class Folder_Name:
    def __init__(self):
        self.folder_name = ""


folder_obj = Folder_Name()


def set_folder_name(new_name, *args, **kwargs):
    global folder_obj
    folder_obj.folder_name = new_name
    os.makedirs(f"tests/{new_name}", exist_ok=True)
