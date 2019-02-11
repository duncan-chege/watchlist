from flask import render_template,request,redirect,url_for,abort
from . import main
from ..request import get_movies,get_movie,search_movie
from .forms import ReviewForm,UpdateProfile
from ..models import Review,User
from flask_login import login_required, current_user
from ..import db,photos    #we will need it when saving profile info changes to our db
import markdown2        #responsible for the conversion from markdown to HTML.

#views
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''

    #The first message on the left of the = sign, represents the variable in the
    #template. The one to the right represents the variable in our view function.

    #Getting popular movie
    popular_movies = get_movies('popular')      #create a variable popular_movies where we call our get_movies() function and pass in "popular" as an argument.
    upcoming_movie = get_movies('upcoming')
    now_showing_movie = get_movies('now_playing')
    viewtitle = "Home- The best Movie review site"
    
    search_movie = request.args.get('movie_query')      # We get the query in our view function using request.args.get()function

    if search_movie:
        return redirect(url_for('search',movie_name=search_movie))
    else:

        return render_template('index.html', title = viewtitle, popular = popular_movies, upcoming = upcoming_movie, now_playing = now_showing_movie) #pass the result from that function call to our template.
                                                        #popular_movies holds the data. popular passes that data in index.html file

@main.route('/movie/<int:id>')
def movie(id):

    '''
    View movie page function that returns the movie details page and its data
    '''
    movie = get_movie(id)
    title = f'{movie.title}'
    reviews = Review.get_reviews(movie.id)      #call the get_reviews class method that takes in a movie ID and will return a list of reviews for that movie

    return render_template('movie.html',title = title,movie = movie, reviews = reviews)     #pass the reviews to our template


# create the search view function that will display our search items from the API.
@main.route('/search/<movie_name>')
def search(movie_name):
    '''
    View function to create search result
    '''
    movie_name_list = movie_name.split(" ")
    movie_name_format = "+".join(movie_name_list)
    searched_movies = search_movie(movie_name_format)
    title = f'search results for {movie_name}'
    return render_template('search.html',movies = searched_movies)

#create a new dynamic route for our new_review function and pass in the movie id
@main.route('/movie/review/new/<int:id>', methods = ['GET','POST'])
@login_required     #This decorator will intercept a request and check if the user is authenticated and if not the user will be redirected to the login page.
def new_review(id):

    form = ReviewForm()     # create an instance of the ReviewForm class and name it form 
    movie = get_movie(id)       #call the get_movie and pass in the ID to get the movie object for the movie with that ID

    if form.validate_on_submit():       #returns True when the form is submitted and all the data has been verified by the validators
        title = form.title.data
        review = form.review.data

        #Updated review instance
        new_review = Review(movie_id=movie.id, movie_title=title, image_path=movie.poster, movie_review=review, user=current_user)

        #Save review model
        new_review.save_review()
        return redirect(url_for('.movie',id = movie.id ))


    title = f'{movie.title} review'

    #If the validate_on_submit() method returns False we will render our new_review.html template file and pass in the title, the form object and the movieobject.
    return render_template('new_review.html', title = title, review_form= form, movie=movie)
    
#creating a profile view function    
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:     #if no user is found
        abort(404)      #404 Not found is returned as a response
    return render_template("profile/profile.html", user = user)  #we pass in the 1st user as a variable

#create a view function that will handle an update request
@main.route('/user/<uname>/update', methods = ['GET','POST'])
@login_required
def update_profile(uname): 
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    
    form = UpdateProfile()      #UpdateProfile form class is instantiated

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))    #redirect the user back to the profile page where he can see the new bio.
    return render_template('profile/update.html',form =form)    #if form is not vaidated, we render the _update.html_ template and pass in the form instance.

@main.route('/user/<uname>/update/pic',methods= ['POST'])       #create a route that will process our form submission request
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()       #query the database to pick a user with the same username we passed in.
    if 'photo' in request.files:        #use the flask request function to check if any parameter with the name photo has been passed into the request.
        filename = photos.save(request.files['photo'])      #saves the file to our applicaion
        path = f'photos/{filename}'     #create a path variable to where the file is stored
        user.profile_pic_path = path    #update the profile_pic_path property in our user table and store the path of the file.
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))        #redirect that "user" back to the profile page.


@main.route('/review/<int:id>')
def single_review(id):      #responsible for handling requests for a single review
    review=Review.query.get(id)     #query the database to get a single review with the the same id as the one passed in
    if review is None:      #check if the review is available
        abort(404)

    #Markdown2 markdown function takes in 2 arguments.
    #1st, the markdown that is being converted, here, we pass in the review.movie_review which is the movie review that is in markdown
    #2nd  is a lists of styling to style the HTML.
    format_review = markdown2.markdown(review.movie_review,extras=["code-friendly", "fenced-code-blocks"])
    
    #render the template and pass in the formatted review.html file 
    return render_template('review.html',review = review,format_review=format_review)