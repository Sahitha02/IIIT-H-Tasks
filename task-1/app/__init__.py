from flask import Flask
from .db import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True  # IMPORTANT: Shows SQL logs

    db.init_app(app)

    with app.app_context():
        from .models import User, Post
        db.create_all()

    from .routes import main
    app.register_blueprint(main)

    return app
