from flask import Blueprint, jsonify
from .models import User

main = Blueprint("main", __name__)

@main.route("/users")
def get_users_bad():
    users = User.query.all()  # 1 query for users
    data = []

    for u in users:
        # Accessing u.posts triggers another query (N queries)
        posts = [{"id": p.id, "title": p.title} for p in u.posts]
        data.append({
            "id": u.id,
            "name": u.name,
            "posts": posts
        })
    
    return jsonify(data)
