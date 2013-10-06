from flask_wtf import Form
from wtforms import TextField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(Form):
    subdomain = TextField("Subdomain:", validators=[DataRequired()])
    api_key = TextField("API-key",  validators=[DataRequired()])
    api_secret = TextField("API-secret",  validators=[DataRequired()])
    submit = SubmitField("Send")