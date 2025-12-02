from flask import Blueprint, jsonify, request, current_app
import time
import json
from sqlalchemy.orm import selectinload
from app.db import db
from .models import User, Post, Segment, SegmentContext
from .pagination import paginate_list, paginate_query
from worker.log_worker import log_action

dash = Blueprint("dash", __name__)

# TASK-8: Annotator Dashboard (with Redis Caching)
@dash.route("/annotator_dashboard")
def annotator_dashboard():
    redis_client = current_app.redis
    cache_key = "annotator_dashboard_cache"

    # 1) Try cache
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    # 2) Heavy computation (simulate slow dashboard)
    data = [i * i for i in range(20000)]

    response = {
        "message": "Annotator dashboard loaded",
        "count": len(data)
    }

    # 3) Cache for 30 seconds
    redis_client.setex(cache_key, 30, json.dumps(response))

    return response


# TASK-8: Reviewer Dashboard (with Redis Caching)
@dash.route("/reviewer_dashboard")
def reviewer_dashboard():
    redis_client = current_app.redis
    cache_key = "reviewer_dashboard_cache"

    # 1) Try cache
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)

    # 2) Query from DB
    users = User.query.all()
    posts = Post.query.all()

    response = {
        "message": "Reviewer dashboard open",
        "users": len(users),
        "posts": len(posts)
    }

    # 3) Store in cache for 30 seconds
    redis_client.setex(cache_key, 30, json.dumps(response))

    return response


# Logbook Simulation (slow)
@dash.route("/logbook")
def logbook():
    total = 0
    for i in range(50000):
        total += (i % 10)
    time.sleep(0.1)
    return jsonify({"total": total})


# TASK-4: Pagination (Annotator)
@dash.route("/annotator_dashboard_paginated")
def annotator_dashboard_paginated():
    page = request.args.get("page", 1)
    limit = request.args.get("limit", 50)

    # heavy computed list
    data = [i * i for i in range(20000)]

    result = paginate_list(data, page, limit)
    result["data"] = list(result["data"])  # make API safe

    return jsonify(result)


# TASK-4: Pagination (Reviewer)
@dash.route("/reviewer_dashboard_paginated")
def reviewer_dashboard_paginated():
    page = request.args.get("page", 1)
    limit = request.args.get("limit", 10)

    users_query = User.query
    posts_query = Post.query

    users_result = paginate_query(users_query, page, limit)
    posts_result = paginate_query(posts_query, page, limit)

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
# -----------------------------------------------------------
# TASK-8: Validator Dashboard (with Redis Caching)
# -----------------------------------------------------------
@dash.route("/validator_dashboard")
def validator_dashboard():
    redis_client = current_app.redis
    cache_key = "validator_dashboard_cache"

    # 1) Try cache
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    # 2) Simulate heavy validator logic
    logs = [{
        "log_id": i,
        "status": "valid" if i % 2 == 0 else "invalid",
        "user_id": i % 10
    } for i in range(50000)]

    valid_count = sum(1 for log in logs if log["status"] == "valid")

    response = {
        "message": "Validator dashboard loaded",
        "total_logs": len(logs),
        "valid_logs": valid_count
    }

    # 3) Cache result for 30 seconds
    redis_client.setex(cache_key, 30, json.dumps(response))

    return response

# TASK-4: Validator dashboard paginated
@dash.route("/validator_dashboard_paginated")
def validator_dashboard_paginated():
    page = request.args.get("page", 1)
    limit = request.args.get("limit", 50)

    logs = [{
        "log_id": i,
        "status": "valid" if i % 2 == 0 else "invalid",
        "user_id": i % 10
    } for i in range(50000)]

    result = paginate_list(logs, page, limit)
    return jsonify(result)


# TASK-5: Aggregated Dashboard Summary
@dash.route("/dashboard_summary")
def dashboard_summary():
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


# TASK-7: Segment Context (slow)
@dash.route("/segment_context/<int:segment_id>")
def segment_context(segment_id):
    segment = Segment.query.get(segment_id)
    if not segment:
        return {"error": "Segment not found"}, 404

    context_list = [{
        "id": ctx.id,
        "text": ctx.text
    } for ctx in segment.contexts]

    return {
        "segment_id": segment.id,
        "segment_name": segment.name,
        "contexts": context_list
    }


# task-7: Segment Context optimized
@dash.route("/segment_context_optimized/<int:segment_id>")
def segment_context_optimized(segment_id):
    segment = (
        Segment.query
        .options(selectinload(Segment.contexts))
        .filter_by(id=segment_id)
        .first()
    )

    if not segment:
        return {"error": "Segment not found"}, 404

    context_list = [
        {"id": ctx.id, "text": ctx.text}
        for ctx in segment.contexts
    ]

    return {
        "segment_id": segment.id,
        "segment_name": segment.name,
        "contexts": context_list
    }

