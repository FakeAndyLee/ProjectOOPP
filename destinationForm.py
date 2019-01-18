from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange


class DestinationForm(FlaskForm):
    journeyName = StringField("Name this Journey", validators=[DataRequired(),
                                                               Length(min=2, max=20, message="Journey Name must be"
                                                                                             "between 2 and 20"
                                                                                             "characters long.")])
    busNumber = IntegerField("Select Bus Number", validators=[DataRequired(), NumberRange(min=2, max=975,
                                                                                          message="Invalid Bus Number")])
    journeyFrom = StringField("Bus Stop Code", validators=[DataRequired()])
    journeyTo = StringField("Destination", validators=[DataRequired()])
    alertMe = IntegerField("Alert Me Before {?} Stops", validators=[DataRequired(), NumberRange(min=1, max=7, message=
                                                                                                "Out of range! Between"
                                                                                                "1 to 7 only")])
    submit = SubmitField("Submit")


class BusRoutes(FlaskForm):
    comment1 = TextAreaField("Comment for the boys", validators=[DataRequired()])
    submit2 = SubmitField("Submit Please")


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    comment = TextAreaField("Feedback:", validators=[DataRequired()])
    submit1 = SubmitField("Submit")