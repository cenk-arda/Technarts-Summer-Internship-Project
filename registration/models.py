from django.db import models


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
    email = models.EmailField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=32)