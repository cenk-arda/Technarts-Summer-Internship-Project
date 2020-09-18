from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=150)

    def __str__(self):
        return self.ingredient_name


class Meal(models.Model):
    meal_name = models.CharField(max_length=150)
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.meal_name


class MyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True)
    about = models.TextField(null=True,blank=True,max_length=250)

    def __str__(self):
        return self.user.username
