from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import User, Feedback, connect_db, db
from forms import RegisterForm, LoginForm, DeleteForm, FeedbackForm

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.route('/')
def redir_register():
    """redirect to register page."""
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register_user():
    """Register user - produce form & handle form submission."""
    form = RegisterForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(name, pwd, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()

        session["username"] = user.username

        # on successful login, redirect to secret page
        return redirect("/secret")

    else:
        return render_template("register.html", form=form)
    
@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")
    
    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(name, pwd)

        if user:
            session["username"] = user.username  # keep logged in
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Bad name/password"]
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)
# end-login

@app.route('/logout')
def logout():
    """Clear session information and log user out."""
    session.pop("username")

    return redirect('/')

@app.route('/users/<username>')
def show_user(username):

    if "username" not in session or username != session['username']:
        flash("You must be logged in to view!")
        return redirect("/")
    
    user = User.query.get(username)
    form = DeleteForm()

    return render_template('users/show.html', user=user, form=form)

@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):

    if "username" not in session or username != session['username']:
        flash("You must be logged in to view!")
        return redirect("/")
    
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect('/login')

@app.route('/users/<username>/feedback/new', methods=["GET", "POST"])
def new_feedback(username):
    """Display feedback form."""

    if "username" not in session or username != session['username']:
        flash("You must be logged in to view!")
        return redirect("/")
    
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    
    else: 
        return render_template("feedback/new.html", form=form)
    
@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Display update feedback form."""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        flash("You must be logged in to view!")
        return redirect("/")
    
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    
    return render_template("feedback/edit.html", form=form, feedback=feedback)

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        flash("You must be logged in to view!")
        return redirect("/")

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")













###################### NOTES ##########################

# Authentication vs Authorization

    # Authentication - verify somebody is who they say they are; ability to sign up, login, or logout of an application

    # Authorization - permissions; you ARE who you say you are, but that doesn't mean you have free reign in an application. User-level limitations/permissions. E.G. User vs Moderator on Reddit.

# Hash()

    # 