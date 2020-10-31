from dotenv import load_dotenv
import json
import time
import os
import datetime
import sys
import signal

sys.path.insert(1, os.path.join(sys.path[0], ".."))
from Parler import Parler, models

load_dotenv(dotenv_path=".parler.env")
parler = Parler(jst=os.getenv("JST"), mst=os.getenv("MST"), debug=False)

interval = 5
filename = "hashtags.json"
if len(sys.argv) > 1:
	filename = sys.argv[1]
with open(filename, mode="a") as hashtags:
	results = []
	def ex(signal, frame):
		print("Closing...")
		hashtags.write(json.dumps(results))
		hashtags.close()
		sys.exit(0)
	signal.signal(signal.SIGINT, ex)
	while True:
		time.sleep(interval)
		results.append({
			"timestamp": str(datetime.datetime.now()),
			"hashtags": parler.hashtags().get("tags")
		})
		
