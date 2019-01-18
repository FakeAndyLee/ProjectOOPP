from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length

class busRoutes(FlaskForm):

    comment = StringField(Length(max=50))
    submit = SubmitField("Submit")
