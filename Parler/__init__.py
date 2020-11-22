import requests
from typing import List
import random
import string
import json

class Parler:


	@staticmethod
	def get_login_key(email, password):
		data = {
			"identifier": email,
			"password": password,
			"deviceId": "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
		}
		response = requests.post('https://api.parler.com/v2/login/new', data=json.dumps(data))
		return response.json()
	
	@staticmethod
	def get_chapta_image(key):
		data = {
			"identifier": key
		}

		response = requests.post('https://api.parler.com/v2/login/captcha/new', data=json.dumps(data))
		return response.json()

	@staticmethod
	def submit_chapta(key, solution):
		data ={
			"identifier": key,
			"solution":solution
		}

		response = requests.post('https://api.parler.com/v2/login/captcha/submit',data=json.dumps(data))
		return response.json()
	"""
	:param jst: short-term token
	:param mst: master token
	:param debug: print debugging messages
	"""
	def __init__(self, jst: str, mst: str, debug: bool):
		self.jst = jst
		self.mst = mst
		self.debug = debug
		self.base_url = "https://api.parler.com/v1"
		self.session = requests.Session()

		self.session.cookies.set("mst", mst)
		self.session.cookies.set("jst", jst)

	"""
	:param username: Username to fetch
	"""
	def profile(self, username=None) -> dict:
		response = self.session.get(self.base_url + "/profile")
		if username is not None:
			params = (
				("username", username),
			)
			response = self.session.get(self.base_url + "/profile", params=params)
		if response.status_code != 200:
			raise Exception({"status": response.status_code})
		return response.json()
	
	"""
	:param searchtag: Hashtag to search
	"""
	def hashtags(self, searchtag="") -> dict:
		params = (
			("search", searchtag),
		)
		response = self.session.get(self.base_url + "/hashtag",  params=params)
		if response.status_code != 200:
			raise Exception({"status": response.status_code})
		return response.json()

	"""
	:param limit: limit
	:param cursor: string to id the next items
	"""
	def feed(self, limit=10, cursor="") -> dict:
		params = (
			("limit", limit),
		)
		if cursor != "":
			params = params + (("startkey",cursor),)
		response = self.session.get(self.base_url + "/feed",  params=params)
		if response.status_code != 200:
			raise Exception({"status": response.status_code})
		return response.json()
		
	"""
	:param limit: limit
	:param cursor: string to id the next items
	"""
	def notifications(self, limit=10, cursor="") -> dict:
		params = (
			("limit", limit),
		)
		if cursor != "":
			params = params + (("startkey",cursor),)
		response = self.session.get(self.base_url + "/notification",  params=params)
		if response.status_code != 200:
			raise Exception({"status": response.status_code})
		return response.json()

	"""
	:param limit: limit
	:param cursor: string to id the next items
	"""
	def discover_feed(self, limit=10, cursor="") -> dict:
		params = (
			("limit", limit),
		)
		if cursor != "":
			params = params + (("startkey",cursor),)
		response = self.session.get(self.base_url + "/discover/posts",  params=params)
		if response.status_code != 200:
			raise Exception({"status": response.status_code})
		return response.json()

	"""
	:param tag: hashtag to get feed from
	:param limit: limit
	:param cursor: string to id the next items
	"""
	def hashtags_feed(self, tag, limit=10, cursor="") -> dict:
		params = (
			("tag", tag),
			("limit", limit)
		)
		if cursor != "":
			params = params + (("startkey",cursor),)
		response = self.session.get(self.base_url + "/post/hashtag",  params=params)
		if response.status_code != 200:
			raise Exception({"status": response.status_code})
		return response.json()