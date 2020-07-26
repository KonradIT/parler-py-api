import requests
from typing import List

class Parler:
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
