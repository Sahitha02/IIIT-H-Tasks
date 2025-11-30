from flask import Flask
from .db import db
from .dashboards import dash
from .profiler_cprofile import profile_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:487755@localhost:5433/tasks'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True  # IMPORTANT: Shows SQL logs

    db.init_app(app)

    with app.app_context():
        from .models import User, Post
        db.create_all()

    from .routes import main
    app.register_blueprint(main)
    app.register_blueprint(dash)
    app.register_blueprint(profile_bp)



    return app
