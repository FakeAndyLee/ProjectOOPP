import functools
import os
from flask import Flask, render_template, flash, url_for, redirect, request, abort, session, send_from_directory
from destinationForm import DestinationForm, ContactForm
from persistence import *
from HomePersistence import *
from FeedbackPersistence import *
from adminhome import AdminForm
from busroutes import *
from commentPersistence import *
import shelve

app = Flask(__name__)
app.secret_key = 'development key'
app.config['SECRET_KEY'] = '4f6c484fa2d098ccb271bf1f07173423'


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session['id'] is None:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view


@app.route('/init')
def init():
    init_db()
    session.clear()
    return 'db initialised'


@app.route("/")
@app.route("/home")
def home():
    session['what'] = 'WHAT'
    session['sup'] = 'nothing'
    temp = 'bus.jpg'
    PList = ["bus.jpg", "download1.jpg", "download3.jpg", "download4.jpg"]
    adminform = AdminForm(request.form)
    with shelve.open("blogs"):
        accessblog = get_blogs()

    # deletestuff = update_blog()
    #retrieve data from storage
    #PList = getPListData()

    return render_template("home.html", tp=temp, Piclist=PList, accessblog=accessblog, adminform=adminform)#deletestuff=deletestuff)


@app.route("/AdminHome", methods=['GET', 'POST'])
def AdminHome():
    # accessblog = get_blogs()
    print('after AdminHome!!!');
    adminform = AdminForm(request.form)
    if 'ADMIN' in session['id']:
        if request.method == 'POST':
            if request.form['submit'] == 'Delete All':
                with shelve.open('blogs') as title:
                    for i in title:

                        delete_blog(i)

                    return render_template("home.html", adminform=adminform, blogs=blogs)

            # elif request.form['submit'] == 'Delete':
            #     with shelve.open('blogs') as title:
            #
            #         for i in title:
            #             if i == i:
            #                 print(i)
            #                 delete_blog(i)
            #
            #             return render_template('home.html', blogs=blogs)

            else:
                if adminform.validate():

                    with shelve.open("blogs"):
                        create_blog(adminform.middle.data, 'bus.jpg')           #(description,picture)
                        accessblog = get_blogs()

                        return render_template("AdminHomePage.html", adminform=adminform, accessblog=accessblog, blogs=blogs)

                else:
                    flash('Input is too long', 'error')
                    return render_template("AdminHomePage.html", adminform=adminform)
        else:
            feedbacks = get_feedbacks()
            return render_template("AdminHomePage.html", adminform=adminform, feedbacks=feedbacks)
    else:
        return redirect(url_for('logout'))


# return render_template("AdminHomePage.html", adminform=adminform, accessblog=accessblog)


def update(id):
    post = get_blog(id)

    if request.method == 'POST':
        description = request.form['description']
        #body = request.form['body']
        error = None

        if not description:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post.description = description
            # post.body = body
            update_blog(post)
            return redirect(url_for('home'))

    return render_template('AdminHomePage.html', post=post)


@app.route('/<string:id>/delete', methods=('GET', 'POST'))
def delete(id):
    delete_blog(id)
    posts = get_blogs()
    # adminform = AdminForm(request.form)
    # create_blog(adminform.middle.data, 'bus.jpg')
    return render_template('home.html', posts=posts)
    # , adminform=adminform)


def update(id):
    post = get_blog(id)

    if request.method == 'POST':
        description = request.form['description']
        #body = request.form['body']
        error = None

        if not description:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post.description = description
            # post.body = body
            update_blog(post)
            return redirect(url_for('home'))

    return render_template('AdminHomePage.html', post=post)


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/testsite")
def testsite():
    return render_template("testsite.html")


@app.route("/hello", methods=["POST"])
def hello():
    name = request.form.get("stops")
    return render_template("hello.html", name=name)


@app.route("/contactus", methods=["GET", "POST"])
def contactus():
    dest = ContactForm(request.form)
    if request.method == "POST":
        if dest.validate():  #.validate_on_submit()
            with shelve.open("feedbacklist") as feedbacklist:
                # feedbacklist["username"] = dest.name.data
                # feedbacklist["feedback"] = dest.comment.data

                id = generate_feedbackID();
                print('*****Feedback...check ID='+id+'!')
                userFeedback = Feedback(id)
                userFeedback.name = dest.name.data
                userFeedback.comment = dest.comment.data
                feedbacklist[userFeedback.id] = userFeedback


            return render_template("feedlist.html", dest=dest)

        else:
            return render_template("contact.html", dest=dest)
    else:
        return render_template("contact.html", dest=dest)


@app.route("/quiz")
def quiz():
    question1 = "1)How many singaporeans travel using public transport??"
    question2 = "2)What are the most popular transport in singapore"
    question3 = "3)how much can you save taking public transport?"
    return render_template("quiz.html", qns1=question1 , qns2=question2, qns3=question3)


@app.route("/help")
def help():
    return render_template("help.html", title="Help")


listofBuses = [{269: {54009: "Ang Mo Kio Int", 54248: "Blk 324", 54239: "Blk 209", 54229: "Ang Mo Kio Pri Sch",
                      54181: "Blk 258", 54191: "Blk 170", 54201: "Opp Blk 155", 54451: "Blk 643", 54461: "Blk 649",
                      55201: "Opp Anderson JC", 55199: "Blk 645", 55169: "Opp Yio Chu Kang Cc", 55019: "The Calrose",
                      55129: "Blk 604", 55119: "Blk 167", 54209: "Bet Blks 152/155", 54199: "Blk 163", }},
               {72: {55329: "Nanyang Poly", 54351: "Nanyang Poly Backgate", 54471: "Opp Blk 538", 54481: "ITE Coll Ctrl",
                     54651: "Opp Techplace 2", 66451: "Aft AMK Ind Pk 2", 66461: "Bef Seagate", 66471: "Bef Yio Chu Kang Rd",
                     64119: "Blk 953", 64491: "Hougang 1", 64481: "Bef Blks 930/931", 64471: "Blk 917", 64419: "Blk 681",
                     64521: "Blk 834", 64559: "Blk 830", 64549: "Opp Hougang Ctrl Int", 64019: "Blk 302", 64201: "Aft Hougang Ave 3"}}]


@app.route("/destination", methods=['GET', 'POST'])
def destination():
    dest = DestinationForm(request.form)
    error = "Bus Code/Number/Destination mismatch!"
    if request.method == "POST":
        if dest.validate():
            with shelve.open('transportStorage') as transportStorage:
                transportStorage['journeyName'] = dest.journeyName.data
                transportStorage['busNumber'] = int(dest.busNumber.data)
                transportStorage['busstopCode'] = int(dest.busstopCode.data)
                transportStorage['destination'] = dest.destination.data
                transportStorage['busID'] = dest.busID.data
                transportStorage['alertMe'] = int(dest.alertMe.data)
            for d in listofBuses:
                for key, value in d.items():
                    if key == dest.busNumber.data:   # key is the bus number , eg 76
                        for busstopCode, place in value.items():    # value is the dict of the bus and bus desc
                            if dest.busstopCode.data == busstopCode:   # over riding the bus stop code with the name
                                dest.busstopCode.data = place      # eg Ang Mo Kio Int
                        for a, b in value.items():
                            if b == dest.destination.data:
                                img = url_for('static', filename=dest.busstopCode.data + " " + dest.destination.data + ".jpg")
                                return render_template("results.html", dest=dest, value=value, img=img)
            else:
                return render_template("destinationForm.html", dest=dest, error=error, listofBuses=listofBuses)
        else:
            return render_template("destinationForm.html", dest=dest, listofBuses=listofBuses)
    else:
        return render_template("destinationForm.html", dest=dest, listofBuses=listofBuses)


@app.route('/busroutenotes')
def comments():
    if request.method =='POST':
        pass
    else:
        comment = get_comments()
        return render_template('busroutenotes.html', comment=comment, busRoutes= busRoutes)


@app.route('/busroutes', methods=['GET', 'POST'])
def comment():
    bus = busRoutes(request.form)
    if request.method == "POST":
        if bus.validate():
            with shelve.open('routeNotes') as routeComment:

                id= generate_commentID()
                print('*****Feedback...check ID='+id+'!')
                userComment= Comment(id)
                userComment.comment1 = bus.comment1.data
                userComment.comment2 = bus.comment2.data
                routeComment[userComment.id] = userComment

                return render_template("busroutenotes.html", bus=bus)

        else:
            return render_template("busroutes.html", bus=bus)
    else:
        return render_template("busroutes.html", bus= bus)


@app.route('/ratings', methods=['GET', 'POST'])
def starRatings():
    starR = starRating(request.form)
    error = None
    if request.method == "POST":
        if starR.validate():
            with shelve.open('starGiven') as starGiven:
                starGiven['stars'] = starR.stars.data

            return render_template("thanks.html", starR=starR)

        else:
            return render_template("ratings.html", starR=starR, error=error)

    return render_template("ratings.html", starR=starR, error=error)


@app.route("/transit")
def transit():
    return render_template("inTransitpage.html", title="Transit")


@app.route("/feedlist")
def feedlist():
    return render_template("feedlist.html", title="Feedlist")


@app.route('/thankyou')
def newpass():
    return render_template('newpass.html')


@app.route('/busdriver', methods=('GET', 'POST'))
def busdriver():
    session['id'] = 'BUSDRIVER'
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        if not username:
            error = 'Enter username plez'
        elif not password:
            error = 'Enter password plez'
        else:
            if username == 'Zhang Jingyuan' and password == 'hellothere':
                session['user_name'] = 'Bus driver'
                return redirect(url_for('home'))
            elif username == 'admin123' and password == 'admin123':
                session['id'] = 'ADMIN'
                session['user_name'] = 'ADMIN'
                return redirect(url_for('home'))
            else:
                error = 'Invalid username or password.'
        flash(error)
    return render_template('busdriver.html')


@app.route('/forgetpassword', methods=('GET', 'POST'))
def forgetpassword():
    session['id'] = 'FORGET'
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        error = None
        if not username:
            error = 'Please enter your username'
        elif not email:
            error = 'Please enter your email'
        else:
            user = get_pass(username, email)
            if user is None:
                error = 'Wrong username or email is entered.'
            else:
                return redirect(url_for('newpass'))
        flash(error)
    return render_template('forgetpassword.html')


@app.route('/login',  methods=('GET', 'POST'))
def login():
    session['id'] = 'LOGIN'
    if session['sup'] == 'CREATED':
        error = 'Account Created!'
        flash(error)
        session['sup'] = 'nothing'
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            error = None
            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'
            else:
                user = get_user(username, password)
                if user is None:
                    error = 'Wrong username or password'
                else:
                    session['email'] = user.get_email()
                    session['id'] = user.get_id()
                    session['user_name'] = user.get_username()
                    session['password'] = user.get_password()
                    return redirect(url_for('home'))
            flash(error)
    return render_template('login.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
    session['id'] = 'REGISTER'
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        confirm = request.form['password2']
        error = None
        if username.isspace() or password.isspace():
            error = 'Username or password cannot be blank.'
        else:
            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'
            elif not email:
                error = 'Email is required'
            elif password != confirm:
                error = "Passwords are not the same"
            else:
                user = getuser(username)
                if user is True:
                    emails = getemail(email)
                    if emails is True:
                        create_user(username, password, email)
                        session['sup'] = 'CREATED'
                        return redirect(url_for('login'))
                    else:
                        error = 'Email is already in use, please choose a new one.'
                else:
                    error = 'Username is already in use, please use a new one'
        flash(error)
    return render_template('register.html')


@app.route('/updateaccount', methods=("GET", "POST"))
def update():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        error = None
        if username.isspace() or password.isspace():
            error = 'Username or password cannot be blank.'
        elif username == '' or password == '':
            error= 'Username or password cannot be blank'
        else:
            user = getuser(username)
            if user is True:
                emails = getemail(email)
                if emails is True:
                    i = session['id']
                    deleteuser(i)
                    create_user(username, password, email)
                    user = get_user(username, password)
                    session['email'] = user.get_email()
                    session['id'] = user.get_id()
                    session['user_name'] = user.get_username()
                    session['password'] = user.get_password()
                    return redirect(url_for('profile'))
                else:
                    error = 'Email is already in use, please choose a new one.'
            else:
                error = 'Username is already in use, please use a new one'
        flash(error)
    return render_template('profile.html')


@app.route('/profile', methods=('GET', 'POST'))
def profile():
    if 'WHAT' in session['what']:
        return redirect(url_for('logout'))
    else:
        return render_template('profile.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    # target = os.path.join(APP_ROOT, 'static/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)

    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("profile.html", image_name=filename)


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)


APP_ROOT = os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":
    app.run(debug=True)


