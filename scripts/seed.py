from app import create_app
from app.db import db
from app.models import User, Post

app = create_app()

def run_seed():
    with app.app_context():
        print("Seeding database...")

        db.drop_all()
        db.create_all()

        u1 = User(name="Alice")
        u2 = User(name="Bob")

        db.session.add_all([u1, u2])
        db.session.commit()

        posts = [
            Post(user_id=u1.id, title="Alice Post 1"),
            Post(user_id=u1.id, title="Alice Post 2"),
            Post(user_id=u2.id, title="Bob Post 1"),
        ]
        db.session.add_all(posts)
        db.session.commit()

        print("Seed complete!")

if __name__ == "__main__":
    run_seed()
