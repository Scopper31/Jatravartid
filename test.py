# var 1
# import sys
# from time import sleep
# for i in range(21):
#     sys.stdout.write("\r")
#     # the exact output you're looking for:
#     sys.stdout.write("[%-20s] %d%%" % ("=" * i, 5 * i))
#     sys.stdout.flush()
#     sleep(0.25)

# var 2
# from progressbar import ProgressBar, Percentage, Bar, Timer
# from time import sleep

# widgets = [Percentage(), " ", Bar(), " ", Timer()]
# bar = ProgressBar(widgets=widgets, maxval=100)
# bar.start()
# for i in range(100):
#     bar.update(i)
#     sleep(0.1)
# bar.finish()

# var 3 самый красивый но для циклов
# from tqdm import tqdm
# import time

# for i in tqdm(range(100), desc="Загрузка данных", leave=True, colour="green"):
#     time.sleep(0.1)
# var 4
# from alive_progress import alive_bar
# import time

# with alive_bar(100, title="Обработка данных") as bar:
#     for i in range(100):
#         time.sleep(0.1)
#         bar()

# import subprocess

# terminal = [
#     "python3 -m venv env\nsource env/bin/activate\npip install -r requirements.txt\ndjango-admin startproject dating_api .\npython manage.py startapp users\npython manage.py startapp matching\npython manage.py startapp messaging\npython manage.py makemigrations\npython manage.py migrate\npython manage.py createsuperuser"
# ]
# subprocess.run(f"cd tests\n cd dating-api \n" + "\n".join(terminal), shell=True)

from utilities import get_ls_r_output

print(get_ls_r_output("tests/restaurant-drf-api"))
