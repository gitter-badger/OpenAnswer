from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Length


class SignupForm(FlaskForm):
    username = StringField(
        'username', validators=[Length(min=3, max=16, message='Username needs to be between 3 and 16 chars long')]
    )