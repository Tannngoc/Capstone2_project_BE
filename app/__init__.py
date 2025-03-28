from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load .env file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '../.env'))

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, static_url_path="/static")
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import main
    app.register_blueprint(main)

    return app



