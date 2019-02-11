# creating our web Form to create Reviews for the movies

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
# import the Required class validator that will prevent the user from submitting the form without Inputting a value
from wtforms.validators import Required


class ReviewForm(FlaskForm):

    title = StringField('Review title', validators=[Required()])
    review = TextAreaField('Movie review')
    submit = SubmitField('Submit')


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.', validators=[Required()])
    submit = SubmitField('Submit')
