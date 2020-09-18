from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from registration.models import MyUser
from .models import Restaurant, RestaurantsMeal, Comment
from .forms import EditProfileForm, AddReviewForm, AddImageForm, ChangeAboutForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import json

# Create your views here.

class RestaurantListView(LoginRequiredMixin, ListView):

    restaurants = Restaurant.objects.all()
    template_name = 'restaurants/restaurant_list.html'

    def get(self, request, *args, **kwargs):
        paginator = Paginator(self.restaurants, 4)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, template_name=self.template_name, context={'restaurants':self.restaurants,'page_obj':page_obj})

class RestaurantView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        print("users likes:", request.user.myuser.likes.all())
        restaurant_id = kwargs['restaurant_id']
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        meals = restaurant.restaurantsmeal_set.all()
        paginator = Paginator(meals, 4)  # Show n meals per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        for meal in page_obj:
            if meal.likes.filter(id=request.user.myuser.id).exists():
                meal.liked = True
            else:
                meal.liked = False
        print(meals[0].likes.filter(id=request.user.myuser.id))
        return render(request, 'restaurants/restaurant.html', context={'page_obj':page_obj,'restaurant': restaurant, 'meals': meals})

    def post(self, request, *args, **kwargs):
        restaurant_id = request.POST.get('restaurant_id')
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        fav_meal = get_object_or_404(RestaurantsMeal, id=request.POST.get('meal_id'))

        if fav_meal.likes.filter(id=request.user.myuser.id).exists():
            fav_meal.likes.remove(request.user.myuser)
            is_liked = False
        else:
            fav_meal.likes.add(request.user.myuser)
            is_liked = True

        if request.is_ajax():
            context = {'likes_count': fav_meal.likes_count(), 'is_liked': is_liked}
            return HttpResponse(json.dumps(context), content_type='application/json')


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        about_form = ChangeAboutForm(prefix="about")
        edit_form = EditProfileForm(prefix="edit")
        image_form = AddImageForm(prefix="image")
        return render(request, 'restaurants/profile.html', context={'edit_form': edit_form, 'image_form': image_form, 'about_form': about_form})

    def post(self, request, *args, **kwargs):
        edit_form = EditProfileForm(request.POST, prefix="edit", instance=request.user)
        image_form = AddImageForm(request.POST, request.FILES, prefix="image", instance=request.user.myuser)
        about_form = ChangeAboutForm(request.POST, prefix="about", instance=request.user.myuser)

        if 'edit_form' in request.POST and edit_form.is_valid():
            edit_form.save()
            return redirect('/profile')
        elif 'image_form' in request.POST and image_form.is_valid():
            image_form.save()
            return redirect('/profile')
        elif 'about_form' in request.POST and about_form.is_valid():
            about_form.save()
            return redirect('/profile')
        return render(request, 'restaurants/profile.html', context={'edit_form': edit_form, 'image_form': image_form, 'about_form':about_form})


"""@login_required(login_url='/registration/accounts/login/')
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
        form = EditProfileForm()
    return render(request, 'restaurants/profile.html', context={'form': form})"""


class MealView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        restaurant_id = kwargs['restaurant_id']
        meal_id = kwargs['meal_id']
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        meal = restaurant.restaurantsmeal_set.get(pk=meal_id)
        comments = meal.comment_set.all()
        paginator = Paginator(comments, 4)  # Show n meals per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        form = AddReviewForm()
        return render(request, 'restaurants/meal.html',
                      context={'restaurant': restaurant, 'meal': meal, 'form': form, 'page_obj':page_obj})

    def post(self, request, *args, **kwargs):
        restaurant_id = kwargs['restaurant_id']
        meal_id = kwargs['meal_id']
        restaurant = Restaurant.objects.get(pk=restaurant_id)
        meal = restaurant.restaurantsmeal_set.get(pk=meal_id)
        form = AddReviewForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.restaurants_meal = meal
            comment.user = request.user
            comment.save()
            return redirect(
                '/restaurants/{restaurant_id}/{meal_id}/'.format(restaurant_id=restaurant_id, meal_id=meal_id))


        else:
            return render(request, 'restaurants/meal.html',
                          context={'restaurant': restaurant, 'meal': meal, 'form': form})


"""@login_required(login_url='/registration/accounts/login/')
def view_meal(request, restaurant_id, meal_id):
    restaurant = Restaurant.objects.get(pk=restaurant_id)
    meal = restaurant.restaurantsmeal_set.get(pk=meal_id);,
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
                  context={'restaurant': restaurant, 'meal': meal, 'form': form})"""


class DeleteCommentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        restaurant_id = kwargs['restaurant_id']
        meal_id = kwargs['meal_id']
        comment_id = kwargs['comment_id']
        comment_to_delete = Comment.objects.get(pk=comment_id)
        comment_to_delete.delete()
        return redirect('/restaurants/{restaurant_id}/{meal_id}/'.format(restaurant_id=restaurant_id, meal_id=meal_id))


class UserView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs['user_id']
        user = User.objects.get(id=user_id)
        myuser = MyUser.objects.get(user=user)
        if (user == request.user):
            return redirect('/profile')

        return render(request, 'restaurants/users.html', context={'myuser': myuser})


"""@login_required(login_url='/registration/accounts/login/')
def delete_review(request, restaurant_id, meal_id, comment_id):
    comment_to_delete = Comment.objects.get(pk=comment_id)
    comment_to_delete.delete()

    return redirect('/restaurants/{restaurant_id}/{meal_id}/'.format(restaurant_id=restaurant_id, meal_id=meal_id))"""

"""class ImageUploadView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        image_form = AddImageForm()
        return render(request, 'restaurants/profile.html', context={'image_form': image_form})

    def post(self, request, *args, **kwargs):
        my_user = MyUser.objects.get(user=request.user)
        image_form = AddImageForm(request.POST, request.FILES, instance=my_user)
        if image_form.is_valid():
            image_form.save()
        return render(request, 'restaurants/profile.html', context={'image_form': image_form})

        # myuser.avatar = form['image']
        # myuser.save()"""


class FavoritesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        fav_meals = request.user.myuser.likes.all()
        paginator = Paginator(fav_meals, 4)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        for meal in page_obj:
            if meal.likes.filter(id=request.user.myuser.id).exists():
                meal.liked = True
            else:
                meal.liked = False
        return render(request, 'restaurants/favorites.html', context={'fav_meals': fav_meals, 'page_obj':page_obj})

    def post(self, request, *args, **kwargs):
        fav_meal = get_object_or_404(RestaurantsMeal, id=request.POST.get('meal_id'))

        if fav_meal.likes.filter(id=request.user.myuser.id).exists():
            fav_meal.likes.remove(request.user.myuser)
            is_liked = False
        else:
            fav_meal.likes.add(request.user.myuser)
            is_liked = True
        if request.is_ajax():
            context = {'likes_count': fav_meal.likes_count(), 'is_liked': is_liked}
            return HttpResponse(json.dumps(context), content_type='application/json')