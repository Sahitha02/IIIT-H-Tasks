from app import create_app
from app.db import db
from app.models import User, Post, Segment, SegmentContext
import random
import string
import time

app = create_app()

def random_text(length=12):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def run_seed_100k():
    with app.app_context():
        print("\n⚠️ Starting 100k Seed Operation...")

        start_time = time.time()

        # WARNING: This wipes database
        print("Dropping existing tables...")
        db.drop_all()
        db.create_all()

        # -------------------------------
        # 1) Seed Users
        # -------------------------------
        print("Seeding 10,000 users...")
        users = [User(name=f"User_{i}") for i in range(10000)]
        db.session.bulk_save_objects(users)
        db.session.commit()

        # Map user IDs (faster lookups)
        user_ids = [u.id for u in User.query.with_entities(User.id).all()]

        # -------------------------------
        # 2) Seed Posts
        # -------------------------------
        print("Seeding 80,000 posts...")
        posts = []
        for i in range(80000):
            posts.append(Post(
                user_id=random.choice(user_ids),
                title="Post_" + random_text(10),
            ))
            # Save in chunks
            if len(posts) >= 5000:
                db.session.bulk_save_objects(posts)
                db.session.commit()
                posts = []
        if posts:
            db.session.bulk_save_objects(posts)
            db.session.commit()

        # -------------------------------
        # 3) Seed Segments
        # -------------------------------
        print("Seeding 5,000 segments...")
        segments = [Segment(name=f"Segment_{i}") for i in range(5000)]
        db.session.bulk_save_objects(segments)
        db.session.commit()

        segment_ids = [s.id for s in Segment.query.with_entities(Segment.id).all()]

        # -------------------------------
        # 4) Seed Segment Context (10,000 rows)
        # -------------------------------
        print("Seeding 10,000 segment contexts...")
        contexts = []
        for i in range(10000):
            contexts.append(SegmentContext(
                segment_id=random.choice(segment_ids),
                text="Context_" + random_text(20)
            ))
            # Save in chunks
            if len(contexts) >= 2000:
                db.session.bulk_save_objects(contexts)
                db.session.commit()
                contexts = []

        if contexts:
            db.session.bulk_save_objects(contexts)
            db.session.commit()

        end_time = time.time()
        print(f"\n✅ DONE! Total time: {round(end_time - start_time, 2)} seconds")

if __name__ == "__main__":
    run_seed_100k()
