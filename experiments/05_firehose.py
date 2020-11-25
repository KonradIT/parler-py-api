## Mimic firehose functionality

from dotenv import load_dotenv
import json
import time
import os
import datetime
import sys
import csv
import traceback 

sys.path.insert(1, os.path.join(sys.path[0], ".."))
from Parler import Parler, models

load_dotenv(dotenv_path=".parler.env")
parler = Parler(jst=os.getenv("JST"), mst=os.getenv("MST"), debug=False)

interval = 1

with open("users_%s.csv" % str(datetime.date.today()), mode="w") as csv_file:

	wroteheader = False

	while True:
		time.sleep(interval)
		done =False 
		while not done:
			try:
				data = parler.users()
				feed = models.UserListSchema().load(data)
			except: 
				time.sleep(5)
			finally: 
				done = True

		for user in feed.users:
			if not wroteheader:
				fieldnames = user.keys()
				try:
					writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=",", quotechar="\"", quoting=csv.QUOTE_MINIMAL)
				except: continue
				writer.writeheader()
				wroteheader=True
			if not user.get("Followed"):
				# follow them
				done = False
				while not done:
					try:
						msg = parler.follow_user(user.get("Username"))
						if msg.get("message") == "Success":
							print("Followed", user.get("Username"))
					except:
						traceback.print_exc() 
						time.sleep(5)
					finally:
						# log for later use
						writer.writerow(user)
						done=True

