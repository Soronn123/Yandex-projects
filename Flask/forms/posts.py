from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField


class PostsForm(FlaskForm):
    type_post = SelectField('Тип поста', choices=["Планеты", "Космические тела", "Звезда", "Галактики", "Ученые"])
    title = StringField('Заголовок', validators=[DataRequired()])
    crat_content = StringField('Краткое описание', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    photo = FileField('Файл картинки')
    submit = SubmitField('Отправить')