from . import db
from werkzeug.security import generate_password_hash,check_password_hash
#generating_password_hash - This function takes in a password and generates a password hash.
#check_password_hash - This function takes in a hash password and a password entered by a user and checks if the password matches to return a True or False response.
from flask_login import UserMixin   #UserMixin class will help us not implement inbuilt methods for ourselves. 
from .import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Movie:
    '''
    Movie class to define Movie Objects
    '''

    def __init__(self,id,title,overview,poster,vote_average,vote_count):
        self.id =id
        self.title = title
        self.overview = overview
        self.poster = "https://image.tmdb.org/t/p/w500/" + poster
        self.vote_average = vote_average
        self.vote_count = vote_count

# saving our reviews to our database

class Review(db.Model):     #pass in the db.Model class to create a connection to our database

    def __init__(self,movie_id,title,imageurl,review):
        self.movie_id = movie_id
        self.title = title
        self.imageurl = imageurl
        self.review = review

    __tablename__=  'reviews'

    id = db.Column(db.Integer,primary_key = True)
    movie_id = db.Column(db.Integer)
    movie_title = db.Column(db.String)
    image_path = db.Column(db.String)
    movie_review = db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)     # use in Python's datetime module to create a timestamp column posted
                                            #datetime.utcnow gets the current time and saves it to our database

    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))       #create Foreign key column where we store the id of the user who wrote the review.

    def save_review(self):      #save the instance of the Review model to the session and commit it to the database
        db.session.add(self)
        db.session.commit()
        # Review.all_reviews.append(self)


    @classmethod
    def clear_reviews(cls):
        Review.all_reviews.clear()

    @classmethod
    def get_reviews(cls,id):
        reviews = Review.query.filter_by(movie_id=id).all()     #take in a movie id 

        # response = []

        # for review in cls.all_reviews:
        #     if review.movie_id == id:
        #         response.append(review)

        return reviews      #retrieve all views & responses for that specific movie.

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique=True,index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))  #create a foreign key
    bio = db.Column(db.String(255))     #new propery for user profile
    profile_pic_path = db.Column(db.String())       #for user profile
    pass_secure = db.Column(db.String(255))  #column a stores passwords
   
    reviews = db.relationship('Review',backref = 'user',lazy = "dynamic")       #define the relationship inside our User model. 
                                    #connecting with the foreign key in review table
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
    def __repr__(self):
        return f'User {self.username}'

    pass_secure = db.Column(db.String(255))


    @property
    def password(self):  #this is a write only class property
        raise AttributeError('You cannot read the password attribute')
    
    @password.setter
    def password(self,password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):   #method that takes in a password, hashes it and compares it to the hashed password to check if they are the same.
        return check_password_hash(self.pass_secure,password)


class Role(db.Model):
    __tablename__ = 'roles'

    id= db.Column(db.Integer, primary_key= True)
    name =db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")  #create a virtual column that will connect with the foreign key

    def __repr__self(self):
        return f'User {self.name}'

