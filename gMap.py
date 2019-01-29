from flask import Flask, render_template, abort, request
from wtforms import SelectField, SubmitField, Form
app = Flask(__name__)


class School:
    def __init__(self, key, name, lat, lng):
        self.key  = key
        self.name = name
        self.lat  = lat
        self.lng  = lng


schools = (
    School('NYP',      'Nanyang Polytechnic',   37.9045286, -122.1445772),
    School('WSS',       'Whitley Secondary',            37.8884474, -122.1155922),
    School('wci',     'Walnut Creek Intermediate', 37.9093673, -122.0580063)
)
schools_by_key = {school.key: school for school in schools}


class schoolForm(Form):
    selectSchool = SelectField("Location of choice:", choices=[('NYP', 'Nanyang Polytechnic'), ('WSS', 'Whitley Secondary')])
    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def index():
    schForm = schoolForm(request.form)
    return render_template('mapTest.html', schForm=schForm)


@app.route("/<school_code>")
def show_school(school_code):
    schForm = schoolForm(request.form)
    school = schools_by_key.get(school_code)
    print('gay')
    if request.method == "POST":
        print('post')
        if schForm.validate():
            print('validate')
            for i in schools:
                print(i)
                if i == schForm.selectSchool.data:
                    return render_template('map.html', schForm=schForm, school=school)

                else:
                    print('no')
                    return render_template('mapTest.html', schForm=schForm, school=school)
        print('yes')
        return render_template('mapTest.html', schForm=schForm, school=school)

    #if school:
     #   return render_template('map.html', school=school)
    ##   abort(404)


app.run(host='localhost', debug=True)