from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired, Length

from .models import User
from sqlalchemy import func


def already_used(form, field):
    if User.query.filter(
        func.lower(User.name) == func.lower(field.data)
    ).all():
        raise ValidationError("この名前は\u200B既に使用されています。")

class RegistrationForm(FlaskForm):
    name = StringField(
        validators=[
            DataRequired(message="文字が\u200B入力されていません。"),
            Length(max=10), already_used
        ], default=""
    )

    def filter_name(form, field):
        return field.strip()