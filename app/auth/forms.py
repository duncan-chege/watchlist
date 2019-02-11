from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField   #import input fields to faciliate user input. 
                                                                    #Boolean field will render a checkbox in our form
from wtforms import ValidationError


#import Validators; Email validator makes sure that the input follows a proper email address structure and the EqualTo helps us in comparing the two password inputs.
from wtforms.validators import Required,Email,EqualTo      
from ..models import User

class RegistrationForm(FlaskForm):      #create a RegistrationForm form class.

    #creating 4 inputs
    email = StringField('Your Email Address',validators=[Required(),Email()])   #pass in the Required and Email validators
    username = StringField('Enter your username',validators = [Required()])
    password = PasswordField('Password',validators = [Required(), EqualTo('password_confirm',message = 'Passwords must match')])    #EqualTo validator passed to make sure both passwords are the same before the form is submitted
    password_confirm = PasswordField('Confirm Passwords',validators = [Required()])
    submit = SubmitField('Sign Up')

    def validate_email(self,data_field):    # takes in the data field and checks our database to confirm there is no user registered with that email address. 
        if User.query.filter_by(email =data_field.data).first():    # If a user with the same email address is found,  a ValidationError is raised
                raise ValidationError('There is an account with that email')

    def validate_username(self,data_field):
        if User.query.filter_by(username = data_field.data).first():    
            raise ValidationError('That username is taken')

class LoginForm(FlaskForm):
    email = StringField('Your Email Address', validators=[Required(), Email()])
    password = PasswordField('Password',validators =[Required()])
    remember = BooleanField('Remember me?')     #to confirm if the user wants to be logged out after the session
    submit = SubmitField('Sign In')
