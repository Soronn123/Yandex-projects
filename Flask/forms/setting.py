from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, FileField, PasswordField, SelectField
from wtforms.validators import DataRequired


class SettingForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    nickname = StringField('Имя', validators=[DataRequired()])
    role = SelectField('Роль', choices=["Пользователь", "Менеджер", "Админ"])
    new_password = PasswordField('Новый пароль')
    old_password = PasswordField('Старый пароль')
    avatar = FileField('Файл с картинкой')
    submit = SubmitField('Сохранить')