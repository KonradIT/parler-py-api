from marshmallow import Schema, fields, ValidationError, post_load, EXCLUDE

class UserItem(Schema):
	Id = fields.Str(data_key="id")
	Bio = fields.Str(data_key="bio")
	Blocked = fields.Bool(data_key="blocked")
	CoverPhoto = fields.Str(data_key="coverPhoto")
	Followed = fields.Bool(data_key="followed")
	Human = fields.Bool(data_key="human")
	Integration = fields.Bool(data_key="integration")
	Joined = fields.Str(data_key="joined")
	Muted = fields.Bool(data_key="muted")
	Name = fields.Str(data_key="name")
	Rss = fields.Bool(data_key="rss")
	Private = fields.Bool(data_key="private")
	ProfilePhoto = fields.Str(data_key="profilePhoto")
	Username = fields.Str(data_key="username")
	Verified = fields.Bool(data_key="verified")
	VerifiedComments = fields.Bool(data_key="verifiedComments")
	Score = fields.Str(data_key="score")
	Interactions = fields.Int(data_key="interactions")

class PostItem(Schema):
	Id = fields.String( data_key="_id")
	Id2 = fields.String( data_key="id")
	At  = fields.Dict(data_key="@")
	Article  = fields.Bool(data_key="article")
	Body  = fields.String(data_key="body")
	Comments  = fields.String(data_key="comments")
	CreatedAt  = fields.String(data_key="createdAt")
	Creator  = fields.String(data_key="creator")
	Depth  = fields.String(data_key="depth")
	DepthRaw  = fields.Int(data_key="depthRaw")
	Hashtags  = fields.List(fields.String(),   data_key="hashtags")
	Impressions  = fields.String(data_key="impressions")
	Links =  fields.List(fields.String(),   data_key="links")
	Preview  = fields.String(data_key="preview")
	Reposts  = fields.String(data_key="reposts")
	ShareLink  = fields.String(data_key="shareLink")
	State  = fields.Int(data_key="state")
	Upvotes  = fields.String(data_key="upvotes")
	Parent  = fields.String(data_key="parent")
	Sponsored  = fields.String(data_key="sponsored")

class Feed():
	def __init__(self, Badge, BadgeString, Last, Next, PendingFollowers, Prev, Items):
		self.badge = Badge
		self.badge_string = BadgeString
		self.last = Last
		self.next = Next
		self.pending_followers = PendingFollowers
		self.prev = Prev
		self.items = Items

class FeedSchema(Schema):
	Badge = fields.Int(data_key="badge")
	BadgeString = fields.String(data_key="badgeString")
	Last = fields.Bool(data_key="last")
	Next = fields.String(data_key="next")
	PendingFollowers = fields.Int(data_key="pendingFollowers")
	Prev = fields.String(data_key="prev")



	Items = fields.List(fields.Nested(PostItem), data_key="posts")
	# Users = fields.List(fields.Nested(UserItem), data_key="users")

	class Meta:
		unknown=EXCLUDE

	@post_load
	def make_feed(self, data, **kwargs):
		return Feed(**data)
