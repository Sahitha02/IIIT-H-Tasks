from .db import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    posts = db.relationship("Post", backref="author")   # lazy-loaded (N+1)

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    title = db.Column(db.String(100))

# -------------------------------
# Segment Models
# -------------------------------
class Segment(db.Model):
    __tablename__ = "segments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    contexts = db.relationship("SegmentContext", backref="segment", lazy=True)

class SegmentContext(db.Model):
    __tablename__ = "segment_contexts"
    id = db.Column(db.Integer, primary_key=True)
    segment_id = db.Column(db.Integer, db.ForeignKey("segments.id"))
    text = db.Column(db.String(500))
