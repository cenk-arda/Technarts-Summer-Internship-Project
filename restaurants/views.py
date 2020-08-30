from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Restaurant, RestaurantsMeal, Comment, Rate
from .forms import EditProfileForm, AddReviewForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

# @login_required(login_url='/registration/accounts/login/')
##def restaurant_list(request):
##  restaurants = Restaurant.objects.all()

# meals = []
# for restaurant in restaurants:
#   meals.append(restaurant.restaurantsmeal_set.all())
##    return render(request, 'restaurants/restaurant_list.html', context={'restaurants': restaurants})


class RestaurantList(LoginRequiredMixin, View):
    restaurants = Restaurant.objects.all()
    template_name = 'restaurants/restaurant_list.html'
    context = {'restaurants': restaurants}

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name, context=self.context)


##@login_required(login_url='/registration/accounts/login/')
##def view_restaurant(request, restaurant_id):
    # id is an attribute that contains the value of the primary key for the model.
    # if none of the fields of a model is set as primary_key=TRUE, django automatically adds a field like that:
    # id = models.AutoField(primary_key=True) -> this is an auto-incrementing primary key.
    # only 1 field can be set as the primary key in a model.

    ##restaurant = Restaurant.objects.get(pk=restaurant_id)
    ##meals = restaurant.restaurantsmeal_set.all()
    ##return render(request, 'restaurants/restaurant.html', context={'restaurant': restaurant, 'meals': meals})


class ViewRestaurant(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        restaurant_id = kwargs['restaurant_id']

        restaurant = Restaurant.objects.get(pk=restaurant_id)
        meals = restaurant.restaurantsmeal_set.all()
        return render(request, 'restaurants/restaurant.html', context={'restaurant': restaurant, 'meals': meals})

@login_required(login_url='/registration/accounts/login/')
def edit_profile(request):
    # Every ModelForm also has a save() method. This method creates and
    # saves a database object from the data bound to the form. A subclass
    # of ModelForm can accept an existing model instance as the keyword argument instance;
    # if this is supplied, save() will update that instance. If it’s not supplied, save() will create a new instance of
    # the specified model:

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/profile')
    else:
        form = EditProfileForm(request.POST, instance=request.user)
    return render(request, 'restaurants/profile.html', context={'form': form})


@login_required(login_url='/registration/accounts/login/')
def view_meal(request, restaurant_id, meal_id):
    restaurant = Restaurant.objects.get(pk=restaurant_id)
    meal = restaurant.restaurantsmeal_set.get(pk=meal_id);
    if request.method == 'POST':
        form = AddReviewForm(request.POST)
        comment = form.save(commit=False)
        comment.restaurants_meal = meal
        comment.user = request.user
        comment.save()
        return redirect('/restaurants/{restaurant_id}/{meal_id}/'.format(restaurant_id=restaurant_id, meal_id=meal_id))
    else:
        form = AddReviewForm()

    return render(request, 'restaurants/meal.html',
                  context={'restaurant': restaurant, 'meal': meal, 'form': form})


@login_required(login_url='/registration/accounts/login/')
def delete_review(request, restaurant_id, meal_id, comment_id):
    comment_to_delete = Comment.objects.get(pk=comment_id)
    comment_to_delete.delete()

    return redirect('/restaurants/{restaurant_id}/{meal_id}/'.format(restaurant_id=restaurant_id, meal_id=meal_id))
