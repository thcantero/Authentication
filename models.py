from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
#from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

bcrypt = Bcrypt()

class User(db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    
    username = db.Column(db.String(20), 
                         unique=True, 
                         nullable=False)
    
    password_hash = db.Column(db.String(256), 
                              nullable=False)
    
    email = db.Column(db.String(120), 
                      unique=True,
                      nullable=False)
    
    first_name = db.Column(db.String(30),
                         nullable=False)
    
    last_name = db.Column(db.String(30),
                         nullable=False)
        
    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
            '''Register user with hashed password and return user'''
            
            hashed = bcrypt.generate_password_hash(pwd)
            
            #turn bytestrung into normal string (unicode utf8)
            hashed_utf8 = hashed.decode("utf8")
            
            return cls(
                username=username,
                password_hash=hashed_utf8,
                email=email,
                first_name= first_name,
                last_name=last_name)
            
    @classmethod
    def authenticate(cls, username, pwd):
        '''Validate that user exists & password is correct.
        
        Return user if valid, else return False'''
        
        u = User.query.filter_by(username=username).first()
        
        if u and bcrypt.check_password_hash(u.password_hash, pwd):
            #return user instance
            return u
        else:
            return False

class Feedback(db.Model):
    
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.String(100), 
                              nullable=False)
    
    content = db.Column(db.Text,
                      nullable=False)
    
    user_id = db.Column(db.Integer, 
                         db.ForeignKey('users.id'),
                         nullable=False)
    
    user = db.relationship('User', backref="feedbacks", cascade='all,delete')
    
    
def connect_db(app):
    '''Connect db to Flask App'''
    db.app = app
    db.init_app(app)
    
   