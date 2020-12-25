from Parler import Parler, models
from dotenv import load_dotenv
from pathlib import Path
from termcolor import colored
import argparse
import os, json, time, traceback


load_dotenv(dotenv_path='.parler.env')
parler = Parler(jst=os.getenv("JST"), mst=os.getenv("MST"), debug=False)

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument(
		'--show', help="profile/hashtags", type=str, required=True)
	parser.add_argument('--summary', dest='summary', action='store_true')
	parser.set_defaults(summary=False)

	parser.add_argument("--term", type=str)
	args = parser.parse_args()

	# DLK hacking
	if args.show == "profile":
		if args.term:
			print(json.dumps(parler.profile(username=args.term), indent=4))
		else:
			print(json.dumps(parler.profile(), indent=4))
	# /DLK hacking
	if args.show == "hashtags":
		if args.term != "":
			if args.summary:
				for tag in parler.hashtags(args.term).get("tags"):
					print(colored(f'- {tag.get("tag")}', "red"), colored(f'({tag.get("totalPosts")})', "cyan"))
				exit()
			print(json.dumps(parler.hashtags(args.term), indent=4))
			exit()
		if args.summary:
			for tag in parler.hashtags().get("tags"):
				print(colored(f'- {tag.get("tag")}', "red"), colored(f'({tag.get("totalPosts")})', "cyan"))
			exit()
		print(json.dumps(parler.hashtags(), indent=4))

	if args.show == "ingest":
		data = parler.feed(limit=100)
		feed = models.FeedSchema().load(data)
		
		count = 0
		while count < 20:
			if args.summary:
				for post in feed.items:
					print("\t", colored(post.get("Id"), "cyan"))
					print("\t>>> Article:", colored(post.get("Article"), "yellow"))
					print("\t>>> Body:", colored(post.get("Body"), "yellow"))
					print("\t>>> Upvotes:", colored(post.get("Upvotes"), "yellow"))
					print("\t>>> Reposts:", colored(post.get("Reposts"), "yellow"))
					print("\t>>> Author:", colored(post.get("Creator"), "yellow"), "\n")
			else:
					print(json.dumps(feed.items, indent=4))
			try:
				more_posts = feed.next
				data = parler.feed(limit=100, cursor=more_posts)
				feed = models.FeedSchema().load(data)
				count += 1
			except:
				traceback.print_exc()
				time.sleep(5)
			finally:
				time.sleep(1)
