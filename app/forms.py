from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from .models import User


class RegisterForm(FlaskForm):
    username = StringField("Ім'я користувача", validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Підтвердження пароля",
        validators=[DataRequired(), EqualTo("password")],
    )
    submit = SubmitField("Зареєструватися")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data.strip()).first():
            raise ValidationError("Користувач з таким ім'ям вже існує.")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.strip().lower()).first():
            raise ValidationError("Користувач з таким email вже існує.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Увійти")


class UploadForm(FlaskForm):
    name = StringField("Назва моделі", validators=[DataRequired(), Length(max=120)])
    stl_file = FileField("STL файл", validators=[FileRequired(), FileAllowed(["stl"], "Лише STL файли.")])
    photo_file = FileField(
        "Фото моделі",
        validators=[FileAllowed(["png", "jpg", "jpeg", "gif", "webp"], "Лише зображення.")],
    )
    description = TextAreaField("Опис моделі", validators=[Length(max=1000)])
    submit = SubmitField("Завантажити")


class DeleteForm(FlaskForm):
    submit = SubmitField("Видалити")
