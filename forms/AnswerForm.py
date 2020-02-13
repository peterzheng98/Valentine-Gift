from flask_wtf import FlaskForm, Form
from wtforms import Form, BooleanField, StringField, validators, SubmitField
from wtforms.validators import DataRequired, Length


class SubmitForm(Form):
    InputField = StringField(validators=[DataRequired(message='不能不填写哟')], render_kw={
        'class': 'form-control',
        'aria-describedby': 'question-label-addon',
        'id': 'question-answer',
        'placeholder': '输入你的答案'
    })
    submit = SubmitField('提交', render_kw={
        'class': 'btn btn-primary form-control'
    })
