from flask import Blueprint, jsonify, current_app
from sqlalchemy.orm import joinedload
from datetime import datetime

from models import db, User, Post

bp = Blueprint("dashboard", __name__)

@bp.route("/dashboard/data", methods=["GET"])
def dashboard_data():
    # Timestamp logging (UTC)
    ts = datetime.utcnow().isoformat() + "Z"
    current_app.logger.info(f"Route /dashboard/data called at {ts}")

 
    users = (
        db.session.query(User)
        .options(joinedload(User.posts))  # prevents N+1
        .all()
    )

    data = []
    for u in users:
        data.append({
            "id": u.id,
            "name": u.name,
            "posts": [{"id": p.id, "title": p.title} for p in u.posts]
        })

    return jsonify({
        "timestamp": ts,
        "user_count": len(data),
        "users": data
    })
@bp.route("/dashboard/create-user", methods=["POST"])
def create_user():
    from flask import request

    data = request.get_json()

    name = data.get("name")
    posts = data.get("posts", [])  # list of post titles

    if not name:
        return {"error": "name is required"}, 400

    # Create user
    new_user = User(name=name)
    db.session.add(new_user)
    db.session.commit()  # commit to get new_user.id

    # Create posts
    for title in posts:
        p = Post(title=title, user_id=new_user.id)
        db.session.add(p)

    db.session.commit()  # save posts

    return {
        "message": "User created successfully",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "posts": posts
        }
    }, 201

