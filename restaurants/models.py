from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.

class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=12)
    image = models.ImageField(null=True)

    # RestaurantInstance.restaurantsmeal_set()

    def __str__(self):
        return self.restaurant_name


class RestaurantsMeal(models.Model):
    meal_name = models.CharField(max_length=150)
    category = models.CharField(max_length=50)
    image = models.ImageField(null=True)
    ##ingredients = models.ManyToManyField(Ingredient)
    restaurant = models.ForeignKey(Restaurant,
                                   on_delete=models.CASCADE)  # if a restaurant is deleted, meals belongs to it will be deleted, too.

    def __str__(self):
        return self.meal_name


class Comment(models.Model):
    restaurants_meal = models.ForeignKey(RestaurantsMeal,
                                         on_delete=models.CASCADE)  # if a meal is deleted, comments belongs to it will be deleted, too.
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)  # if a user is deleted, comments of her/him will be deleted, too.
    text = models.CharField(max_length=250)
    date = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.text


"""class Rate(models.Model):
    point = models.IntegerField()
    restaurants_meal = models.ForeignKey(RestaurantsMeal,
                                         on_delete=models.CASCADE)  # if a meal is deleted, rate(s) belongs to it will also be deleted.

    def __str__(self):
        return self.point"""
