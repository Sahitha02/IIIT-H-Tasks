from flask import Blueprint, jsonify
import time
from .models import User, Post

dash = Blueprint("dash", __name__)

# Simulate annotator dashboard (slow: heavy loop)
@dash.route("/annotator_dashboard")
def annotator_dashboard():
    data = []
    for i in range(20000):   # simulate heavy processing
        x = i * i
        data.append(x)
    return jsonify({"message": "Annotator dashboard loaded", "count": len(data)})


# Simulate reviewer dashboard (slow: multiple DB reads)
@dash.route("/reviewer_dashboard")
def reviewer_dashboard():
    users = User.query.all()
    posts = Post.query.all()
    time.sleep(0.2)  # simulate wait
    return jsonify({"users": len(users), "posts": len(posts)})


# Simulate logbook (slow: logging + computation)
@dash.route("/logbook")
def logbook():
    total = 0
    for i in range(50000):
        total += (i % 10)
    time.sleep(0.1)
    return jsonify({"total": total})
