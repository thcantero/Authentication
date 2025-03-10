from flask_wtf import FlaskForm
from wtforms import StringField, DateField, EmailField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length


#Class Name that inherits from FlaskForm
class CreateUser(FlaskForm):
    '''Form to Register to the site'''
    
    username = StringField('Username',
                       validators=[InputRequired(message='Field cannot be empty'),
                                   Length(5)])
    
    password = PasswordField('Password',
                       validators=[InputRequired(message='Field cannot be empty'),
                                   Length(5)])
    
    #email not mandatory on the db
    email = EmailField('Email', 
                       validators=[InputRequired(message='Field cannot be empty')])
    
    first_name = StringField('Name',
                       validators=[InputRequired(message='Field cannot be empty'),
                                   Length(3)])
    
    last_name = StringField('Last Name',
                       validators=[InputRequired(message='Field cannot be empty'),
                                   Length(3)])
    
    
class UserLogin(FlaskForm):
    '''Form to Login to the site'''
    
    username = StringField('Username',
                       validators=[InputRequired(message='Field cannot be empty'),
                                   Length(5)])
    
    password = PasswordField('Password',
                       validators=[InputRequired(message='Field cannot be empty'),
                                   Length(5)])
    

class Feedback(FlaskForm):
    '''Form to add feedback'''
    
    title = StringField('Title',
                        validators=[InputRequired(message='Field cannot be empty')])
    
    content = TextAreaField('Feedback',
                        validators=[InputRequired(message='Field cannot be empty')])