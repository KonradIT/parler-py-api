from Parler import Parler, models
from dotenv import load_dotenv
from pathlib import Path
from termcolor import colored
import argparse
import os, json, time


load_dotenv(dotenv_path='.parler.env')
parler = Parler(jst=os.getenv("JST"), mst=os.getenv("MST"), debug=False)

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument(
		'--show', help="profile/hashtags", type=str)

	args = parser.parse_args()

	if args.show == "profile":
		print(json.dumps(parler.profile(), indent=4))
	if args.show == "hashtags":
		print(json.dumps(parler.hashtags(), indent=4))
	if args.show == "ingest":
		data = parler.feed()
		feed = models.FeedSchema().load(data)
		for post in feed.items:
			print(colored(post.get("Id"), "cyan"))
			if post.get("Article"):
				print(colored(post.get("Body"), "yellow"))

