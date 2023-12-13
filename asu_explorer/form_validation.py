from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError

from .models import User
from sqlalchemy import func


class RegistrationForm(FlaskForm):
    name = StringField()

    def validate_name(form, field):
        field.data = field.data.strip()

        if field.data == "":
            raise ValidationError("文字が\u200B入力されていません。")

        if 10 < len(field.data):
            raise ValidationError("10字以内で\u200B入力してください。")

        if User.query.filter(
            func.lower(User.name) == func.lower(field.data)
        ).all():
            raise ValidationError("この名前は\u200B既に使用されています。")