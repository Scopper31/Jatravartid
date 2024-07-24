import google.generativeai as genai

# gemini конфигурация
API_KEY = "AIzaSyDDc_34aQhK3sikAgQJqXsvxyRmGsxKdfQ"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

#variables
folder_name = ''


def set_folder_name(new_name):
    global folder_name
    folder_name = new_name