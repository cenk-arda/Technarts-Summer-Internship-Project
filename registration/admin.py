from django.contrib import admin
from .models import Meal, Ingredient, MyUser

# Register your models here.

admin.site.register(Ingredient)
admin.site.register(Meal)
admin.site.register(MyUser)