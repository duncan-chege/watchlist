from flask import Flask, render_template,request,redirect,url_for
from app import app
from .request import get_movies,get_movie,search_movie   #import the get_movies() function from the request module.Now we get the popular movie from our API.
from .models import reviews
from .forms import ReviewForm
Review = reviews.Review

#views
@app.route('/')
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

@app.route('/movie/<int:id>')
def movie(id):

    '''
    View movie page function that returns the movie details page and its data
    '''
    movie = get_movie(id)
    title = f'{movie.title}'
    reviews = Review.get_reviews(movie.id)      #call the get_reviews class method that takes in a movie ID and will return a list of reviews for that movie

    return render_template('movie.html',title = title,movie = movie, reviews = reviews)     #pass the reviews to our template


# create the search view function that will display our search items from the API.
@app.route('/search/<movie_name>')
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
@app.route('/movie/review/new/<int:id>', methods = ['GET','POST'])
def new_review(id):

    form = ReviewForm()     # create an instance of the ReviewForm class and name it form 
    movie = get_movie(id)       #call the get_movie and pass in the ID to get the movie object for the movie with that ID

    if form.validate_on_submit():       #returns True when the form is submitted and all the data has been verified by the validators
        title = form.title.data
        review = form.review.data
        new_review = Review(movie.id, title, movie.poster, review)
        new_review.save_review()
        return redirect(url_for('movie',id = movie.id))

    title = f'{movie.title} review'

    #If the validate_on_submit() method returns False we will render our new_review.html template file and pass in the title, the form object and the movieobject.
    return render_template('new_review.html', title = title, review_form= form, movie=movie)
    