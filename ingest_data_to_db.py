from Parler import Parler, models
from dotenv import load_dotenv
from pathlib import Path
from termcolor import colored
import os, json, time, traceback
import db

load_dotenv(dotenv_path='.parler.env')

parler = Parler(jst=os.getenv("JST"), mst=os.getenv("MST"), debug=False)
postgres = db.Database(os.getenv("DB_USERNAME"), os.getenv("DB_PASSWORD"))
last_id = postgres.get("last_id")[0]

data = parler.feed(limit=100)
feed = models.FeedSchema().load(data)

ids = [x.get("Id") for x in feed.items]
while last_id not in ids:
	try:
		for post in feed.items:
			postgres.insert(postgres.statements("insert_post"), ())
		more_posts = feed.next
		data = parler.feed(limit=100, cursor=more_posts)
		feed = models.FeedSchema().load(data)
	except:
		traceback.print_exc()
		time.sleep(5)
	finally:
		time.sleep(1)