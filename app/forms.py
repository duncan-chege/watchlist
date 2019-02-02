# creating our web Form to create Reviews for the movies

from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Required     # import the Required class validator that will prevent the user from submitting the form without Inputting a value

class ReviewForm(FlaskForm):

    title = StringField('Review title', validators=[Required()])
    review =TextAreaField('Movie review', validators=[Required()])
    submit =SubmitField('Submit')

