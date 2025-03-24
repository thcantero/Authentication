"""Flask app pplication that lets users sign up and log in to their own accounts. 
Once logged in, users can add feedback, edit their feedback, delete their feedback, 
and see a list of all feedback that they’ve given."""

from flask import Flask, request, jsonify, render_template, session, flash, redirect
from models import db, connect_db, User, Feedback
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS
from forms import UserLogin, CreateUser, Feedback_Form, Edit_Form
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///authentication'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

with app.app_context():
    db.create_all()
   

#GET / : Redirect to /register 
@app.route('/')
def home():
    return redirect('/register')


#GET /login: Show a form that when submitted will login a user. This form should accept 
# a username and a password. Make sure you are using WTForms and that your password input
# hides the characters that the user is typing!

#POST /login: Process the login form, ensuring the user is authenticated and going 
# to /secret if so.
@app.route('/login', methods=['GET', 'POST'])
def login():
    '''This should render the landing page with the following options:
        -Login
        -Register to create a new account
    '''
    
    form = UserLogin()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate(username, password)
        
        if user:
            flash(f"Welcome Back, {user.username}! :)", 'success')
            session['user_id'] = user.id
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors=['Invalid username/password']
  
    return render_template("login.html", form=form)

#GET /register: Show a form that when submitted will register/create a user. 
# This form should accept a username, password, email, first_name, and last_name. 
# Make sure you are using WTForms and that your password input hides the characters that the user is typing!

#POST /register: Process the registration form by adding a new user. Then redirect to /secret
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = CreateUser()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken. Please pick another')
            return render_template('register.html', form=form)
        
        session['user_id'] = new_user.id
        flash('Welcome! You have successfully created an account', 'success')
        return redirect(f'/users/{username}')
        
    return render_template('register.html', form=form)

#GET /logout : Clear any information from the session and redirect to /
@app.route('/logout')
def logout_user():
   
    session.pop('user_id')
    flash("Successfully logged out! See you next time!", 'info')
    return redirect('/')

# --------- Feedback routes ------------

# **GET /users/<username>: Show information about the given user. 
# Show all of the feedback that the user has given. For each piece of feedback,
# display with a link to a form to edit the feedback and a button to delete the feedback. 
# Have a link that sends you to a form to add more feedback and a button to delete the user 
# Make sure that only the user who is logged in can successfully view this page.

#route homepage & keep a user logged in 
@app.route('/users/<username>')
def show_feedback(username):
    if "user_id" not in session:
        flash("Please login or register to see the content", 'danger')
        return redirect ('/')
    
    user = User.query.filter_by(username=username).first_or_404()

    return render_template('user.html', feedback = user.feedbacks, user=user)
    

# POST /users/<username>/delete:
# Remove the user from the database and make sure to also delete all of their feedback. 
# Clear any user information in the session and redirect to /. 
# Make sure that only the user who is logged in can successfully delete their account.
@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    if "user_id" not in session:
        flash("Please login or register to see the content",'danger')
        return redirect ('/')
    
    user = User.query.filter_by(username=username).first_or_404()
    
    for fb in user.feedbacks:
        db.session.delete(fb)
            
    db.session.delete(user)
    db.session.commit()
        
    session.pop('user_id')
    flash("User deleted!", "info")
    return redirect("/")


# GET /users/<username>/feedback/add: Display a form to add feedback 
# Make sure that only the user who is logged in can see this form.
# POST /users/<username>/feedback/add: Add a new piece of feedback and redirect to /users/<username> 
# —Make sure that only the user who is logged in can successfully add feedback.

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST']) 
def add_feedback(username):
    if "user_id" not in session:
        flash("Please login or register to see the content",'danger')
        return redirect ('/')
    
    form = Feedback_Form()
    all_feedback = Feedback.query.all()
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_feedback = Feedback(title=title, content=content, user_id = session['user_id'])
        
        db.session.add(new_feedback)
        db.session.commit()
        flash('Feedback Added!','success')
        return redirect(f'/users/{username}')
    
    return render_template('add-feedback.html', form=form)
    
       

# GET /feedback/<feedback-id>/update: Display a form to edit feedback 
# Make sure that only the user who has written that feedback can see this form
# POST /feedback/<feedback-id>/update: Update a specific piece of feedback and redirect to /users/<username> 
# —Make sure that only the user who has written that feedback can update it.

@app.route('/users/feedback/<int:id>/update', methods=['GET', 'POST'])
def update_feedback(id):
    if "user_id" not in session:
        flash("Please login or register to see the content",'danger')
        return redirect ('/')
    
    feedback = Feedback.query.get_or_404(id)
    username = feedback.user.username
    form = Edit_Form(obj=feedback)
    
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        
        flash('Feedback updated!')
        return redirect(f'/users/{username}')
    
    return render_template('add-feedback.html', form=form, feedback=feedback)
        

# POST /feedback/<feedback-id>/delete: Delete a specific piece of feedback and redirect to /users/<username> 
# —Make sure that only the user who has written that feedback can delete it.
@app.route('/feedback/<int:id>/delete', methods=['POST'])
def delete_feedback(id):
    """Delete the feedback"""
    
    feedback = Feedback.query.get_or_404(id)
    username = feedback.user.username
    
    if feedback.user_id == session['user_id']:
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback deleted!",'info')
    
        return redirect(f'/users/{feedback.user.username}')
    else:
        flash("You don't have permission to delete this feedback",'danger')
        return redirect('/')