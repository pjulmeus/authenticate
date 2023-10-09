from flask import Flask, request, redirect, render_template, session
from models import db, connect_db, User, Feedback
from flask_debugtoolbar import DebugToolbarExtension
from forms import CreateForm, Log_in, FeedbackForm, UpdateFeedbackForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///models_user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

# db.session.drop_all()
# db.session.create_all()

@app.route('/')
def homepage():
        return redirect('/register')

@app.route('/register', methods = ["GET", "POST"])
def create_user():
    form = CreateForm()
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
           
        new_user = User.register(username, password, email, first_name, last_name)
       

        db.session.add(new_user)
        db.session.commit()
        session["username"] = new_user.username
        return redirect(f'/user/{new_user.username}')   
    else:
        return render_template("register.html", form = form)

    
@app.route('/login', methods = ["GET", "POST"])
def log_in_page():
    form = Log_in()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User.authenticate(username, password)

        if new_user:
            session["username"] = new_user.username
            print(session["username"])
            return redirect(f'/user/{new_user.username}')
        else:
            form.username.errors = ["Bad name/password"]
            form.password.errors = ["Wrong/password"]

    return render_template("login.html", form = form)

@app.route('/user/<username>')
def authorized(username):
    if "username" not in session:
        return redirect('/')
    else:
        auth_user = User.query.filter_by(username=session['username']).first()
        feedback = Feedback.query.filter_by(username=session['username']).all()
        return render_template("secret.html", user = auth_user, feedback = feedback)
    
@app.route('/users/<username>/feedback/add', methods = ["GET", "POST"])
def add_feedback_form(username):
    if "username" not in session:
        return redirect('/')
    
    form = FeedbackForm()

    if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            new_feedback = Feedback(title = title, content = content, username = session['username'])
            db.session.add(new_feedback)
            db.session.commit()
            return redirect(f"/user/{new_feedback.username}")
    else:
            return render_template("add_form.html", form = form)
    
@app.route('/users/<username>/feedback/<int:feedback_id>/update', methods = ["GET", "POST"])
def update_form(username, feedback_id):
    if "username" not in session:
        return redirect('/')
    
    form = UpdateFeedbackForm()
    feedbacks = Feedback.query.get(feedback_id)
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        
        feedbacks.title = title
        feedbacks.content = content
        db.session.commit()
        return redirect(f"/user/{username}")
    
    else:
         return render_template("update_form.html", form = form, feedbacks = feedbacks)

@app.route('/users/<username>/feedback/<int:feedback_id>/delete', methods = ["POST"])
def delete(username, feedback_id) :
     feedbacks = Feedback.query.get(feedback_id)
     db.session.delete(feedbacks)
     db.session.commit()
     return redirect(f'/user/{username}')
    
@app.route('/logout')
def log_out():
    session.pop("username")
    return redirect('/')