# holy crap

import logging
from dotenv import load_dotenv
import time
import os
import sys
import threading
import datetime
import random
sys.path.insert(1, os.path.join(sys.path[0], ".."))
from Parler import Parler, models
import traceback
import exputils
import requests
from os.path import splitext
load_dotenv(dotenv_path=".parler.env")
parler = Parler(jst=os.getenv("JST"), mst=os.getenv("MST"), debug=True)
def save_file(link, fname):
	with open("media/" + fname + splitext(link)[1], "wb") as f:
		print("Downloading %s" % fname)
		response = requests.get(link, stream=True)
		total_length = response.headers.get('content-length')

		if total_length is None: # no content length header
			f.write(response.content)
		else:
			dl = 0
			total_length = int(total_length)
			for data in response.iter_content(chunk_size=4096):
				dl += len(data)
				f.write(data)
				done = int(50 * dl / total_length)
				sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
				sys.stdout.flush()
	print("\nFile downloaded!")
hashtags = [
	
	"capitol",
	"USCapitol",
	"stormthecapitol",
	"stormthecapital",
	"@TheProudBoys",
	"@ProudBoysUncensored"
]

filename = "data/hashtags2/%s_%s_%s.csv"
max_sleep_limit= 2

logging.basicConfig(level=logging.DEBUG)
def get_posts(search_hit):
	print("Starting collection of posts with hashtag %s" % search_hit)
	time.sleep(random.randint(1, max_sleep_limit))
	while True:
		try:
			if "@" not in search_hit:
				data = parler.hashtags_feed(search_hit, 100, cursor="")
				feed = models.FeedSchema().load(data)
			else:
				userdetails = parler.profile(search_hit.replace("@", ""))
				data = parler.user_feed(userdetails.get("_id"), 100, cursor="")
				feed = models.FeedSchema().load(data)
			break
		except:
			traceback.print_exc()
			time.sleep(max_sleep_limit)
	with open(filename % (search_hit, str(datetime.date.today()), "posts"), mode="a", encoding="utf-8") as posts:
		exputils.writetocsv(posts, feed.items, insert_headers=True)
	with open(filename % (search_hit, str(datetime.date.today()), "users"), mode="a", encoding="utf-8") as users:
		exputils.writetocsv(users, feed.users, insert_headers=True)
	with open(filename % (search_hit, str(datetime.date.today()), "links"), mode="a", encoding="utf-8") as links:
		exputils.writetocsv(links, feed.links, insert_headers=True)
		
	for link in feed.links:
		if "image-cdn.parler.com" in link.get("Long"): #hosted by parler!
			save_file(link.get("Long"), link.get("Id"))
		if "video.parler.com" in link.get("Long"): #hosted by parler!
			save_file(link.get("Long"), link.get("Id"))    
	while True:
		if feed.last:
			logging.info("Exiting, all done.")
			break
		time.sleep(random.randint(max_sleep_limit/2, max_sleep_limit))
		try:
			if "@" not in search_hit:
				data = parler.hashtags_feed(search_hit, 100, cursor="")
				feed = models.FeedSchema().load(data)
			else:
				userdetails = parler.profile(search_hit.replace("@", ""))
				data = parler.user_feed(userdetails.get("_id"), 100, cursor="")
				feed = models.FeedSchema().load(data)
			
		except:
			traceback.print_exc()
			time.sleep(max_sleep_limit)
		finally:
			logging.info("Writing to file...")
			with open(filename % (search_hit, str(datetime.date.today()), "posts"), mode="a", encoding="utf-8") as posts:
				exputils.writetocsv(posts, feed.items, insert_headers=False)
			with open(filename % (search_hit, str(datetime.date.today()), "users"), mode="a", encoding="utf-8") as users:
				exputils.writetocsv(users, feed.users, insert_headers=False)
			with open(filename % (search_hit, str(datetime.date.today()), "links"), mode="a", encoding="utf-8") as links:
				exputils.writetocsv(links, feed.links, insert_headers=False)
			for link in feed.links:
				if "image-cdn.parler.com" in link.get("Long"): #hosted by parler!
					save_file(link.get("Long"), link.get("Id"))
				if "video.parler.com" in link.get("Long"): #hosted by parler!
					save_file(link.get("Long"), link.get("Id"))    

for search_hit in hashtags:
	thr = threading.Thread(target=get_posts, args=(search_hit,))
	thr.start()
