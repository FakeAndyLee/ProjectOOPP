#from flask_wtf import Form0
#FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, Form
from wtforms.validators import DataRequired, Length


#class AdminForm(FlaskForm):
class AdminForm(Form):
    #photo = FileField(validators=[FileRequired()])
    middle = StringField('Name of top-right title (Announcement)', validators=[DataRequired(), Length(max=200)])
    #.label
    submit = SubmitField("Add")
