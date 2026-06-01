from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.models import User


class RegisterForm(FlaskForm):
    username = StringField(
        "Kullanıcı Adı", validators=[DataRequired(), Length(min=3, max=64)]
    )
    email = StringField("E-posta", validators=[DataRequired(), Email()])
    password = PasswordField("Şifre", validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField(
        "Şifre (Tekrar)", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Kayıt Ol")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Bu kullanıcı adı zaten kullanılıyor.")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Bu e-posta adresi zaten kayıtlı.")


class LoginForm(FlaskForm):
    email = StringField("E-posta", validators=[DataRequired(), Email()])
    password = PasswordField("Şifre", validators=[DataRequired()])
    remember_me = BooleanField("Beni hatırla")
    submit = SubmitField("Giriş Yap")
