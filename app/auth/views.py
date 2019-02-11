from flask import render_template,redirect,url_for,flash,request    #flash function helps us display error messages to the user
from . import auth
from ..models import User
from .forms import RegistrationForm,LoginForm
from .. import db
from flask_login import login_user,logout_user,login_required
from ..email import mail_message

@auth.route('/login',methods=['GET','POST'])
def login():
    login_form = LoginForm()

    #check if the form is validated where we search for a user from our database with the email we receive from the form.
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):   # use the verify_password method to confirm that the password entered matches with the password hash stored in the database.
            login_user(user,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or Password')

    title = "watchlist login"
    return render_template('auth/login.html',login_form = login_form,title=title)  #will render a template file

@auth.route('/register',methods = ["GET","POST"])
def register():
    form = RegistrationForm()      #created the form instance
    if form.validate_on_submit():
        
        #When the form is submitted we create a new user from the User model and pass in the email,username and password. 
        user = User(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(user)        #add the new user to the session
        db.session.commit()     #commit the session to add the user to our db

        # Sending a welcome email
        mail_message("Welcome to watchlist","email/welcome_user",user.email,user=user)      #pass in the the subject and template file where our message body will be stored.
                                     #We then pass in the new user's email address which we get from the registration form. We then pass in a user as a keyword argument.


        return redirect(url_for('auth.login'))
        title = "New Account"
    return render_template('auth/register.html',registration_form = form)

@auth.route('/logout')      #route logout that calls the flask_login's logout_user function
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))      #redirect the user to the index page.
