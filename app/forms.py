from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SessionForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    submit = SubmitField('Enter Chanel')