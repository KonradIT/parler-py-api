from marshmallow import Schema, fields, ValidationError, post_load, EXCLUDE, INCLUDE
import json


class UserItem(Schema):
    Id = fields.Str(data_key="id", default="", missing="")
    Bio = fields.Str(data_key="bio", default="", missing="")
    Blocked = fields.Bool(data_key="blocked", default="", missing="")
    CoverPhoto = fields.Str(data_key="coverPhoto", default="", missing="")
    Followed = fields.Bool(data_key="followed", default="", missing="")
    Human = fields.Bool(data_key="human", default="", missing="")
    Integration = fields.Bool(data_key="integration", default="", missing="")
    Joined = fields.Str(data_key="joined", default="", missing="")
    Muted = fields.Bool(data_key="muted", default="", missing="")
    Name = fields.Str(data_key="name", default="", missing="")
    Rss = fields.Bool(data_key="rss", default="", missing="")
    Private = fields.Bool(data_key="private", allow_none=True)
    ProfilePhoto = fields.Str(data_key="profilePhoto", default="", missing="")
    Username = fields.Str(data_key="username", default="", missing="")
    Verified = fields.Bool(data_key="verified", default="", missing="")
    VerifiedComments = fields.Bool(data_key="verifiedComments", default="", missing="")
    Score = fields.Str(data_key="score", default="", missing="")
    Interactions = fields.Int(data_key="interactions", default="", missing="")

    class Meta:
        unknown = EXCLUDE


class PostItem(Schema):
    Id = fields.String(data_key="_id", default="", missing="")
    Id2 = fields.String(data_key="id", default="", missing="")
    At = fields.Dict(data_key="@", default="", missing="")
    Article = fields.Bool(data_key="article", default="", missing="")
    Body = fields.String(data_key="body", default="", missing="")
    Color = fields.String(data_key="color", default="", missing="")
    CommentDepth = fields.Int(data_key="commentDepth", default="", missing="")
    Commented = fields.Bool(data_key="commented", default="", missing="")
    Comments = fields.String(data_key="comments", default="", missing="")
    Controversy = fields.Int(data_key="controversy", default="", missing="")
    Conversation = fields.String(data_key="conversation", default="", missing="")
    CreatedAt = fields.String(data_key="createdAt", default="", missing="")
    Creator = fields.String(data_key="creator", default="", missing="")
    Depth = fields.String(data_key="depth", default="", missing="")
    DepthRaw = fields.Int(data_key="depthRaw", default="", missing="")
    Downvotes = fields.String(data_key="downvotes", default="", missing="")
    Hashtags = fields.List(fields.String(), data_key="hashtags", default="", missing="")
    Impressions = fields.String(data_key="impressions", default="", missing="")
    IsPrimary = fields.Bool(data_key="isPrimary", default="", missing="")
    Links = fields.List(fields.String(), data_key="links", default="", missing="")
    Post = fields.String(data_key="post", default="", missing="")
    Preview = fields.String(data_key="preview", default="", missing="")
    ReplyingTo = fields.String(data_key="replyingTo", default="", missing="")
    Reposted = fields.Bool(data_key="reposted", default="", missing="")
    Reposts = fields.String(data_key="reposts", default="", missing="")
    ShareLink = fields.String(data_key="shareLink", default="", missing="")
    State = fields.Int(data_key="state", default="", missing="")
    Upvotes = fields.String(data_key="upvotes", default="", missing="")
    Parent = fields.String(data_key="parent", default="", missing="")
    Score = fields.String(data_key="score", default="", missing="")
    Sponsored = fields.String(data_key="sponsored", default="", missing="")
    Sensitive = fields.Bool(data_key="sensitive", default="", missing="")
    Root = fields.String(data_key="root", default="", missing="")
    Voted = fields.String(data_key="voted", default="", missing="")

    class Meta:
        unknown = EXCLUDE


class LinkItem(Schema):
    Id = fields.String(data_key="_id")
    CreatedAt = fields.String(data_key="createdAt")
    Domain = fields.String(data_key="domain")
    Long = fields.String(data_key="long")

    Modified = fields.String(data_key="modified")
    Short = fields.String(data_key="short")
    State = fields.String(data_key="state")

    class Meta:
        strict = True
        unknown = INCLUDE
        postprocess = True


class Feed:
    def __init__(
        self,
        Badge,
        BadgeString,
        Last,
        Next,
        PendingFollowers,
        Prev,
        Items=None,
        Item=None,
        Comments=None,
        Users=None,
        Links=None,
    ):
        self.badge = Badge
        self.badge_string = BadgeString
        self.last = Last
        self.next = Next
        self.pending_followers = PendingFollowers
        self.prev = Prev
        self.items = Items
        self.item = Item
        self.comments = Comments
        self.users = Users
        self.links = Links


class FeedSchema(Schema):
    """For newsfeed, user posts, or user comments."""

    Badge = fields.Int(data_key="badge")
    BadgeString = fields.String(data_key="badgeString")
    Last = fields.Bool(data_key="last")
    Next = fields.String(data_key="next")
    PendingFollowers = fields.Int(data_key="pendingFollowers")
    Prev = fields.String(data_key="prev")
    Items = fields.List(fields.Nested(PostItem), data_key="posts", allow_none=True)
    Item = fields.Nested(PostItem, data_key="post", allow_none=True)
    Comments = fields.List(
        fields.Nested(PostItem), data_key="comments", allow_none=True
    )
    Users = fields.List(fields.Nested(UserItem), data_key="users", allow_none=True)
    Links = fields.List(fields.Nested(LinkItem), data_key="urls", allow_none=True)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_feed(self, data, **kwargs):
        return Feed(**data)


class UserList:
    def __init__(self, Users, Last, Next, Prev):
        self.users = Users
        self.last = Last
        self.next = Next
        self.prev = Prev


class UserListSchema(Schema):
    Users = fields.List(fields.Nested(UserItem), data_key="users")
    Last = fields.Bool(data_key="last")
    Next = fields.String(data_key="next")
    Prev = fields.String(data_key="prev")

    @post_load
    def make_userlist(self, data, **kwargs):
        return UserList(**data)
