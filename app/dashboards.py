from flask import Blueprint, jsonify
import time
from app import db
from .models import User, Post
from flask import request
from .pagination import paginate_list
from .pagination import paginate_query
from redis import Redis
from worker.log_worker import log_action


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
    log_action.send(1, "opened reviewer dashboard")
    time.sleep(0.2)  # simulate wait
    return jsonify({
        "message": "Reviewer dashboard open",
        "users": len(users),
        "posts": len(posts) 
        })


# Simulate logbook (slow: logging + computation)
@dash.route("/logbook")
def logbook():
    total = 0
    for i in range(50000):
        total += (i % 10)
    time.sleep(0.1)
    return jsonify({"total": total})
#task-4
@dash.route("/annotator_dashboard_paginated")
def annotator_dashboard_paginated():
    page = request.args.get("page", 1)
    limit = request.args.get("limit", 50)

    # heavy computed list
    data = [i * i for i in range(20000)]

    result = paginate_list(data, page, limit)

    # convert into API-safe format
    result["data"] = list(result["data"])

    return jsonify(result)
@dash.route("/reviewer_dashboard_paginated")
def reviewer_dashboard_paginated():
    page = request.args.get("page", 1)
    limit = request.args.get("limit", 10)

    # Query with pagination
    users_query = User.query
    posts_query = Post.query

    users_result = paginate_query(users_query, page, limit)
    posts_result = paginate_query(posts_query, page, limit)

    # Convert SQLAlchemy models to dict
    users_data = [{"id": u.id, "name": u.name} for u in users_result["data"]]
    posts_data = [{"id": p.id, "title": p.title, "user_id": p.user_id} for p in posts_result["data"]]

    return jsonify({
        "users": {
            "page": users_result["page"],
            "limit": users_result["limit"],
            "total_items": users_result["total_items"],
            "total_pages": users_result["total_pages"],
            "data": users_data
        },
        "posts": {
            "page": posts_result["page"],
            "limit": posts_result["limit"],
            "total_items": posts_result["total_items"],
            "total_pages": posts_result["total_pages"],
            "data": posts_data
        }
    })

@dash.route("/validator_dashboard_paginated")
def validator_dashboard_paginated():
    page = request.args.get("page", 1)
    limit = request.args.get("limit", 50)

    # Large simulated log list
    logs = [{
        "log_id": i,
        "status": "valid" if i % 2 == 0 else "invalid",
        "user_id": i % 10
    } for i in range(50000)]

    result = paginate_list(logs, page, limit)

    return jsonify(result)

# task - 5
@dash.route("/dashboard_summary")
def dashboard_summary():
    # Optimized aggregated JOIN query
    results = (
        db.session.query(
            User.id,
            User.name,
            db.func.count(Post.id).label("post_count")
        )
        .outerjoin(Post, User.id == Post.user_id)
        .group_by(User.id)
        .order_by(User.id)
        .all()
    )

    # Convert result rows to dict format
    posts_per_user = [
        {
            "user_id": row[0],
            "user_name": row[1],
            "post_count": row[2]
        }
        for row in results
    ]

    total_users = db.session.query(db.func.count(User.id)).scalar()
    total_posts = db.session.query(db.func.count(Post.id)).scalar()

    return {
        "total_users": total_users,
        "total_posts": total_posts,
        "posts_per_user": posts_per_user
    }
