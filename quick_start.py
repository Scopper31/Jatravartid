import subprocess

commands = """
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
"""
subprocess.run(commands, shell=True)
