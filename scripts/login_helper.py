import sys, os

sys.path.insert(1, os.path.join(sys.path[0], ".."))

import Parler
import configparser
import logging

config_file = "./parlerconfig.ini"
logging.basicConfig(level=logging.INFO)

parler = Parler.Parler(debug=True)

print("Parler v3 API Login Helper tool")
print("Please enter your email used to register with Parler")
email = input("Email: ").strip()

sendMagicLinkResp = parler.send_magic_link(email)
magicLinkGot = input("Magic link: ")

gotOTP = parler.seed_login(magicLinkGot)

token = parler.magic_login(gotOTP)

config = configparser.ConfigParser()
config.read(config_file)
config.set("credentials", "token", token)

with open(config_file, "w") as cf:
    config.write(cf)
print("All done.")
