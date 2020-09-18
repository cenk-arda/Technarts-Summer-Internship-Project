from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from registration.models import MyUser
from django.db.models import Avg, Count


# Create your models here.

class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=12)
    image = models.ImageField(null=True)

    # RestaurantInstance.restaurantsmeal_set()

    def __str__(self):
        return self.restaurant_name

    def get_model_type(self):
        return "Restaurant"


class RestaurantsMeal(models.Model):
    likes = models.ManyToManyField(MyUser, related_name="likes",blank=True)
    meal_name = models.CharField(max_length=150)
    category = models.CharField(max_length=50)
    image = models.ImageField(null=True)
    price = models.FloatField(null=True, blank=True)
    meal_info = models.CharField(max_length=200, blank=True, null=True)
    ##ingredients = models.ManyToManyField(Ingredient)

    # if a restaurant is deleted, meals belongs to it will be deleted, too.
    restaurant = models.ForeignKey(Restaurant,
                                   on_delete=models.CASCADE)

    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return self.meal_name

    def average_rate(self):
        average_rate = Comment.objects.filter(restaurants_meal=self).aggregate(avg=Avg('rate'))
        average = 0
        if average_rate['avg'] is not None:
            average = average_rate['avg']
        return average

    def get_model_type(self):
        return "RestaurantsMeal"


class Comment(models.Model):
    # if a meal is deleted, comments belongs to it will be deleted, too.
    restaurants_meal = models.ForeignKey(RestaurantsMeal,
                                         on_delete=models.CASCADE)
    rate = models.IntegerField(default=1)
    # if a user is deleted, comments of her/him will be deleted, too.
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    date = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.text

    def get_model_type(self):
        return "Comment"


"""class Rate(models.Model):
    point = models.IntegerField()
    restaurants_meal = models.ForeignKey(RestaurantsMeal,
                                         on_delete=models.CASCADE)  # if a meal is deleted, rate(s) belongs to it will also be deleted.

    def __str__(self):
        return self.point"""
