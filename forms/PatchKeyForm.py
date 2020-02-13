from flask_wtf import FlaskForm, Form
from wtforms import Form, BooleanField, StringField, validators, SubmitField
from wtforms.validators import DataRequired, Length


class PatchKeyForm(Form):
    Key1 = StringField(validators=[DataRequired(message='不能不填写哟')], render_kw={
        'class': 'form-control',
        'aria-describedby': 'question-label-addon-1',
        'id': 'question-answer-1',
        'placeholder': '输入你的答案'
    })
    Key2 = StringField(validators=[DataRequired(message='不能不填写哟')], render_kw={
        'class': 'form-control',
        'aria-describedby': 'question-label-addon-2',
        'id': 'question-answer-2',
        'placeholder': '输入你的答案'
    })
    Key3 = StringField(validators=[DataRequired(message='不能不填写哟')], render_kw={
        'class': 'form-control',
        'aria-describedby': 'question-label-addon-3',
        'id': 'question-answer-3',
        'placeholder': '输入你的答案'
    })
    submit = SubmitField('提交', render_kw={
        'class': 'btn btn-primary form-control'
    })
