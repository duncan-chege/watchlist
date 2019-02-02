# create the Reviews class inside our models folder.

class Review:
    
    all_reviews = []

    def __init__(self,movie_id,title,imageurl,review):
        self.movie_id = movie_id
        self.title = title
        self.imageurl = imageurl
        self.review = review

    def save_review(self):
        Review.all_reviews.append(self)

    @classmethod
    def clear_reviews(cls):         #class method that clears all items from the list
        Review.all_reviews.clear()
        
    @classmethod
    def get_reviews(cls,id):        #new class method that takes an ID

        response = []
        for review in cls.all_reviews:      #loops thru all reviews in the all_reviews list and checks for reviews that have the same movie ID as the ID passed
            if review.movie_id == id:
                response.append(review)     #we append those reviews to a new response list

        return response     #we return that response list