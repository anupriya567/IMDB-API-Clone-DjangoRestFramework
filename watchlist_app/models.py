from django.db import models
from django.contrib.auth.models import User
from django.core.validators  import MinValueValidator,MaxValueValidator

# Each model is a Python class that subclasses django.db.models.Model.


class StreamPlateform(models.Model):
    name = models.CharField(max_length=50)
    about = models.CharField(max_length=500)
    website = models.URLField(default =True)

    def __str__(self):
        return self.name

class WatchList(models.Model): 
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=500)
    plateform = models.ForeignKey(StreamPlateform, on_delete = models.CASCADE, related_name="watchlist")
    active = models.BooleanField(default =True)
    created = models.DateTimeField(auto_now_add=True)
    avg_rating = models.FloatField(default = 0)
    number_rating  = models.IntegerField(default = 0)

    def __str__(self):
        return self.title

        
class Review(models.Model):
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description = models.CharField(max_length=500)
    watchlist = models.ForeignKey(WatchList, on_delete = models.CASCADE, related_name="reviews")
    active = models.BooleanField(default= True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    review_user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.rating) + " | " + self.watchlist.title + " | " + str(self.review_user)


    

