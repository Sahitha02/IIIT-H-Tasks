from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
from models import db
from routes import bp as dashboard_bp
import os

def create_app():
    app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'app.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SQLALCHEMY_ECHO'] = True

    db.init_app(app)

    app.register_blueprint(dashboard_bp)

    sql_logger = logging.getLogger('sqlalchemy.engine')

    sql_handler = RotatingFileHandler(
        "sql.log",
        maxBytes=5_000_000,   # 5 MB
        backupCount=3
    )
    sql_handler.setLevel(logging.INFO)

    sql_format = logging.Formatter("%(asctime)s - %(message)s")
    sql_handler.setFormatter(sql_format)

    sql_logger.addHandler(sql_handler)
    sql_logger.setLevel(logging.INFO)

    handler = RotatingFileHandler("access.log", maxBytes=1000000, backupCount=3)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)