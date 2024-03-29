# .env
from dotenv import load_dotenv

load_dotenv(override=True)

# app, config
import os, json

from flask import Flask


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

# db, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

db = SQLAlchemy(app)
from .models import User

app.config.update(
    SESSION_TYPE="sqlalchemy", SESSION_SQLALCHEMY=db
)
sess = Session(app)

with app.app_context():
    db.create_all()

# monkey patch
from flask_admin._compat import pass_context
from flask_admin.model.base import BaseModelView

@pass_context
def get_list_value(self, context, model, name):
    return str(self._get_list_value(
        context, model, name,
        self.column_formatters,
        self.column_type_formatters
    ))

BaseModelView.get_list_value = get_list_value

#/home/asuexplorer/.local/lib/python3.10/site-packages/
path = f"{os.environ['VIRTUAL_ENV']}/Lib/site-packages/flask_admin/templates/bootstrap2/admin/model/list.html"
with open(path, mode="r", encoding="utf-8") as f:
    lines = f.readlines()
    lines[146] = "{{ get_value(row, c)|truncate(50) }}\n"

with open(path, mode="w", encoding="utf-8") as f:
    f.writelines(lines)

# admin
from flask_admin import Admin
from flask_basicauth import BasicAuth

from .auth_model_view import AuthModelView


admin = Admin(app)
basic_auth = BasicAuth(app)
admin.add_views(
    AuthModelView(User, db.session, basic_auth),
    AuthModelView(sess.app.session_interface.sql_session_model, db.session, basic_auth)
)

from . import views