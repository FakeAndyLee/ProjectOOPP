from flask_wtf import *
from wtforms import *
from wtforms.validators import DataRequired, Length


class busRoutes(Form):

    comment1 = StringField("comment1", validators=[Length(max=50)])
    comment2 = StringField("comment2", validators=[Length(max=50)])
    submit3 = SubmitField("Submit")
    submit4 = SubmitField("Submit")

class starRating(Form):

    stars = RadioField('', choices=[('1', '✪'), ('2', '✪✪'), ('3', '✪✪✪'), ('4', '✪✪✪✪'), ('5', '✪✪✪✪✪')])
    submits = SubmitField("Submit")
