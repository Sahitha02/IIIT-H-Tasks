from flask import Blueprint, jsonify
import time
from .models import User, Post
from flask import request
from .pagination import paginate_list
from .pagination import paginate_query

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
