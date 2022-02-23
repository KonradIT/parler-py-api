import sys, os

sys.path.insert(1, os.path.join(sys.path[0], ".."))

import Parler
from Parler import with_auth as authed
import time, random, threading
import logging

logging.basicConfig(level=logging.INFO)

required_envs = ["PARLER_USERNAME", "PARLER_PASSWORD"]

for envvar in required_envs:
	assert os.getenv(envvar) != None

parler = Parler.Parler(debug=True)
parler_auth = authed.AuthSession(debug=False)
parler_auth.login(
	identifier=os.getenv("PARLER_USERNAME"), password=os.getenv("PARLER_PASSWORD")
)

assert parler_auth.is_logged_in

def follow_badged_users():
	time.sleep(random.randint(1,30))
	r = parler_auth.trending_users()
	for user in r:
		time.sleep(random.randint(1,3))
		logging.info("username: %s badges: %s " % (user.get("username"), user.get("badges")))
		if (
			(user.get("badges").get("parler_emp") != 0
			or user.get("badges").get("verified") != 0
			or user.get("badges").get("gold") != 0
			or user.get("badges").get("early") != 0) and user.get("badges").get("rss") == 0
		):
			r = parler_auth.follow_user(user.get("username"))
			print(r)
		

for _ in range(0, 100):
	thr = threading.Thread(target=follow_badged_users)
	thr.start()
