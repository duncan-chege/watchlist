from flask import render_template
from . import main

@main.errorhandler(404)       #new decorator app.errorhandler() passes in the error we receive.
def four_Ow_four(error):        #created a view function
    '''    
    Function to render the 404 error page
    '''

    return render_template('fourOwfour.html'),404