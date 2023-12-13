# .env
from dotenv import load_dotenv

load_dotenv(override=True)

# app, config, CORS
import os, json

from flask import Flask
from flask_cors import CORS


app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)
ANS_COORDS = json.loads(os.getenv("ANS_COORDS"))

app.config.update(
    SECRET_KEY=os.getenv("SECRET_KEY"),
    BASIC_AUTH_USERNAME=os.getenv("USERNAME"),
    BASIC_AUTH_PASSWORD=os.getenv("PASSWORD"),
    SQLALCHEMY_DATABASE_URI="sqlite:///project.db"
)
CORS(app, resources={
    "/static/images/panorama/*": {"origins": "https://cdn.pannellum.org"}
})

# db
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)
from .models import User

with app.app_context():
    db.create_all()

# admin
from flask_admin import Admin
from flask_basicauth import BasicAuth

from .auth_model_view import AuthModelView


admin = Admin(app)
basic_auth = BasicAuth(app)

admin.add_view(AuthModelView(User, db.session, basic_auth))

from . import views