from app import create_app
from models import db, User, Post

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    users = []
    for i in range(1, 6):   
        u = User(name=f"User {i}")
        db.session.add(u)
        users.append(u)
    db.session.commit()

    for u in users:
        for j in range(1, 4):
            p = Post(title=f"Post {j} by {u.name}", user_id=u.id)
            db.session.add(p)
    db.session.commit()

    print("Sample data created.")
