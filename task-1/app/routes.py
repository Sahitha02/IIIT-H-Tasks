from flask import Blueprint, jsonify
from .models import User
from sqlalchemy.orm import selectinload

main = Blueprint("main", __name__)

# ----------------------------------------------------
# TASK 1 — BAD ROUTE WITH N+1 PROBLEM
# ----------------------------------------------------
@main.route("/users")
def get_users_bad():
    users = User.query.all()   # 1 query
    data = []

    for u in users:
        # Accessing u.posts → N more queries (N+1 problem)
        posts = [{"id": p.id, "title": p.title} for p in u.posts]
        data.append({
            "id": u.id,
            "name": u.name,
            "posts": posts
        })

    return jsonify(data)

# ----------------------------------------------------
# TASK 2 — OPTIMIZED ROUTE (FIXED using selectinload)
# ----------------------------------------------------
@main.route("/users_optimized")
def get_users_optimized():
    # FIX: only 1 additional query instead of N queries
    users = User.query.options(selectinload(User.posts)).all()

    data = []
    for u in users:
        posts = [{"id": p.id, "title": p.title} for p in u.posts]
        data.append({
            "id": u.id,
            "name": u.name,
            "posts": posts
        })

    return jsonify(data)

























# from flask import Blueprint, jsonify
# from .models import User

# main = Blueprint("main", __name__)

# @main.route("/users")
# def get_users_bad():
#     users = User.query.all()  # 1 query for users
#     data = []

#     for u in users:
#         # Accessing u.posts triggers another query (N queries)
#         posts = [{"id": p.id, "title": p.title} for p in u.posts]
#         data.append({
#             "id": u.id,
#             "name": u.name,
#             "posts": posts
#         })
    
#     return jsonify(data)
