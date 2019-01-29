from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, SelectField, Form, validators
from wtforms.validators import DataRequired, Length, NumberRange


class DestinationForm(Form):
    journeyName = StringField("Name this Journey", validators=[DataRequired(),
                                                               Length(min=2, max=20, message="Journey Name must be"
                                                                                             " between 2 and 20"
                                                                                             " characters long.")])
    busNumber = IntegerField("Select Bus Number", validators=[DataRequired()])

    busstopCode = IntegerField("Bus Stop Code", validators=[DataRequired(message="Invalid Bus Code!")])
    destination = StringField("Destination", validators=[DataRequired(), Length(min=2, max=20, message="Invalid Destination!")])
    busID = StringField("Bus Plate Number:", validators=[DataRequired(), Length(min=5, max=8, message="Invalid Bus ID!")])
    alertMe = SelectField("Alert me before: ", choices=[('1', '1 Stop'), ('2', '2 Stops'), ('3', '3 Stops'), ('4', '4 Stops'), ('5', '5 Stops')],
                          validators=[DataRequired()])
    submit = SubmitField("Submit")


class BusRoutes(FlaskForm):
    comment1 = TextAreaField("Comment for the boys", validators=[DataRequired(), Length(min=2, max=50)])
    submit2 = SubmitField("Submit Please")


class ContactForm(Form):
    name = StringField("Name", validators=[DataRequired()])
    comment = TextAreaField("Feedback:", validators=[DataRequired()])
    submit1 = SubmitField("Submit")
