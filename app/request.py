#Getting data int our API
import urllib.request,json     #will help us create a connection to our API URL and send a request and json modules that will format the JSON response to a Python dictionary
from .models import Movie



#Getting api key
api_key = None

#Getting the movie base url
base_url= None

def configure_request(app):
    global api_key,base_url
    api_key = app.config['MOVIE_API_KEY']
    base_url = app.config['MOVIE_API_BASE_URL']

def get_movies(category):
    '''
    Function that gets the json response to our url request
    '''
    get_movies_url = base_url.format(category,api_key)      #This will replace the {} curly brace placeholders in the base_url with the category and api_key respectively.

    with urllib.request.urlopen(get_movies_url) as url:         #sends a request as a url
        get_movies_data= url.read()
        get_movies_response = json.loads(get_movies_data)

        movie_results = None

        if get_movies_response['results']:      #results contains movie objects
            movie_results_list = get_movies_response['results']     #process_results() function that takes in the list of dictionary objects and returns a list of movie objects.
            movie_results = process_results(movie_results_list)        #return movie_results which is a list of movie objects.

    return movie_results

#Processing results
def process_results(movie_list):
    '''
    Function  that processes the movie result and transform them to a list of Objects

    Args:
        movie_list: A list of dictionaries that contain movie details

    Returns :
        movie_results: A list of movie objects
    '''
    movie_results = []
    for movie_item in movie_list:
        id = movie_item.get('id')
        title = movie_item.get('original_title')
        overview = movie_item.get('overview')
        poster = movie_item.get('poster_path')
        vote_average = movie_item.get('vote_average')
        vote_count = movie_item.get('vote_count')

        if poster:
            movie_object = Movie(id,title,overview,poster,vote_average,vote_count)
            movie_results.append(movie_object)

    return movie_results

def get_movie(id):      #function that takes in a movie id and returns a movie object
    get_movie_details_url = base_url.format(id,api_key)     #create a get_movie_details URL by formatting the base URL with the id and API key

    with urllib.request.urlopen(get_movie_details_url) as url:      #create a request
        movie_details_data = url.read()                     
        movie_details_response = json.loads(movie_details_data)     #load the data

        movie_object = None                                 #create a new movie object
        if movie_details_response:
            id = movie_details_response.get('id')
            title = movie_details_response.get('original_title')
            overview = movie_details_response.get('overview')
            poster = movie_details_response.get('poster_path')
            vote_average = movie_details_response.get('vote_average')
            vote_count = movie_details_response.get('vote_count')

            movie_object = Movie(id,title,overview,poster,vote_average,vote_count)

    return movie_object

#create the search request
def search_movie(movie_name):
    search_movie_url = 'https://api.themoviedb.org/3/search/movie?api_key={}&query={}'.format(api_key,movie_name)
    with urllib.request.urlopen(search_movie_url) as url:       #create the request
        search_movie_data = url.read()
        search_movie_response = json.loads(search_movie_data)

        if search_movie_response['results']:        #process the results
            search_movie_list = search_movie_response['results']
            search_movie_results = process_results(search_movie_list)

    return search_movie_results




    
