from Parler import Parler, models

from dotenv import load_dotenv
from pathlib import Path
from termcolor import colored
import argparse

print(colored("Parler login initialization helper script"))
email = input("Email: ")
pwd = input("Password: ")

r = Parler.get_login_key(email, pwd)
login_key = r.get("key")

r = Parler.get_chapta_image(login_key)
print("Chapta time! Copy the following text into https://base64.guru/converter/decode/image")
print(r.get("image"))

chapta = input("What does it say?: ")

