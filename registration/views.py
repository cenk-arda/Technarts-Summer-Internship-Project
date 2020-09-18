from django.shortcuts import render, redirect
from .forms import UserCreationForm  ## this is the overridden form with email field included
## from django.contrib.auth.forms import UserCreationForm ## we don't need this anymore
from django.contrib.auth.models import User
from django.views import View
from restaurants.models import Restaurant, RestaurantsMeal, Comment
from .models import MyUser, User
from django.db.models import Q
from django.db.models import Count, Avg
from datetime import datetime, timedelta
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import numpy as np
import pandas as pd
import sklearn
from sklearn.decomposition import TruncatedSVD
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, View):
    # comments = Comment.objects.all().values()
    # data = pd.DataFrame(comments)
    # data = data.drop_duplicates(["user_id", "restaurants_meal_id"], keep="last")
    # meal_mat = data.pivot_table(index="user_id", columns="restaurants_meal_id", values="rate", fill_value=0)
    # similarmeals = meal_mat.corr(method='pearson')
    #
    # # def get_similar_meals(self,meal_name,user_rating):
    # #     similar_score = self.similarmeals['restaurants_meal_id']*(user_rating-2.5)
    # #     similar_score = similar_score.sort_values(ascending=False)
    # #
    # #     return similar_score

    def get(self, request, *args, **kwargs):
        # print(request.user.comment_set.all().values())

        last_max_rate = 0
        last_liked_meal = []
        for comment in request.user.comment_set.all():
            print("user comments", comment)
            if comment.rate >= last_max_rate:
                last_max_rate = comment.rate
                last_liked_meal = comment.restaurants_meal

        comments = Comment.objects.all().values()
        pearson_correlated_meals = []
        suggested_meals_svd = []

        if last_max_rate:
            data = pd.DataFrame(comments)
            ## keep only the last comment of a user on a specific meal.
            data = data.drop_duplicates(["user_id", "restaurants_meal_id"], keep="last")

            meal_mat = data.pivot_table(index="user_id", columns="restaurants_meal_id", values="rate", fill_value=0)
            print(meal_mat)
            transposed_mat = meal_mat.T
            ## passing random_state = 7 to get the same repeatable results
            svd = TruncatedSVD(n_components=3, random_state=17)
            # [4, 11, 22, 26, 32, 35, 38, 39]
            # n components = 2: [2, 3, 11, 23, 26, 35, 39]
            result_matrix = svd.fit_transform(transposed_mat)
            correlation_matrix = np.corrcoef(result_matrix)
            print("correlation_matrix: \n ", correlation_matrix)

            meal_ids = meal_mat.columns

            meals_id_list = list(meal_ids)
            pivot_meal = last_liked_meal.id
            idx_of_pivot = meals_id_list.index(pivot_meal)
            corr_pivot = correlation_matrix[idx_of_pivot]
            # corr_pivot[::-1].sort()
            print("corr_pivot: \n", corr_pivot)
            print("type of corr_pivot:", type(corr_pivot))
            recommended_ids_svd = list(meal_ids[(corr_pivot < 1.0) & (corr_pivot > 0.9)])

            print("recommended_ids_SVD: \n", recommended_ids_svd)
            print("meal_ids:", meal_ids)

            suggested_meals_svd = []

            for meal_id in recommended_ids_svd:
                meal = RestaurantsMeal.objects.get(id=meal_id)
                # print(meal)
                li = meal.comment_set.filter(user=request.user)
                # print(li)
                if not li:  # or li.exists()
                    suggested_meals_svd.append(meal)

            if (last_liked_meal):
                rates = pd.DataFrame(data.groupby('restaurants_meal_id')['rate'].mean())
                # print("rates w/o rating count: ",rates)
                rates['rating count'] = pd.DataFrame(data.groupby('restaurants_meal_id')['rate'].count())
                # print(rates)
                # print("Pivot meal of user (last and most rated meal):", last_liked_meal, last_liked_meal.id)
                user_ratings_of_meal = meal_mat[last_liked_meal.id]
                # print("request.user id:", request.user.id)
                # print("user ratings of last liked meal id:", user_ratings_of_meal)

                ## Pearson R Correlation Method
                similarmeals = meal_mat.corrwith(user_ratings_of_meal, method='pearson')
                # print("similarmeals(corr with pearson method:\n",similarmeals)

                corr_similar = pd.DataFrame(similarmeals, columns=["Correlation"])
                corr_similar.dropna(inplace=True)

                corr_similar = corr_similar.join(rates['rating count']).sort_values('Correlation', ascending=False)
                # print(corr_similar)
                #
                pearson_correlated_meals = []
                for meal_id in corr_similar.index.tolist()[1:]:
                    meal = RestaurantsMeal.objects.get(id=meal_id)
                    # print(meal)
                    li = meal.comment_set.filter(user=request.user)
                    # print(li)
                    if not li:  # or li.exists()
                        pearson_correlated_meals.append(meal)

                        # print(specific_meal_rates)

        most_reviewed_meals = RestaurantsMeal.objects.annotate(comment_count=Count('comment')).order_by(
            '-comment_count')[:4]
        top_rated_four = []
        for meal in RestaurantsMeal.objects.all():
            top_rated_four.append(meal)
        top_rated_four = sorted(top_rated_four, key=lambda item: item.average_rate(), reverse=True)[:4]

        return render(request, 'registration/home.html',
                      context={'most_reviewed_meals': most_reviewed_meals, 'top_rated_four': top_rated_four,
                               'pearson_correlated_meals': pearson_correlated_meals[:4],
                               'suggested_meals_SVD': suggested_meals_svd})


class SignUpView(View):
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid() and form.mail_is_unique():
            form.save()
            return redirect('login')
        return render(request, self.template_name, {'form': form})


class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')

        if query is not None:
            categories = RestaurantsMeal.objects.filter(Q(category__icontains=query))
            restaurants = Restaurant.objects.filter(Q(restaurant_name__icontains=query))

            meals = RestaurantsMeal.objects.filter(Q(meal_name__icontains=query))
            users = MyUser.objects.filter(Q(user__username__icontains=query) | Q(user__first_name__icontains=query) | Q(
                user__last_name__icontains=query) | Q(user__email__icontains=query))
            items = list(categories) + list(restaurants) + list(meals) + list(users)
            print(sorted(items, key=lambda x: (isinstance(x, RestaurantsMeal))))
            page_number1 = request.GET.get('page1')
            paginator1 = Paginator(restaurants, 6)

            # paginator = Paginator(sorted(items, key=lambda x: (isinstance(x, RestaurantsMeal))), 6)
            try:
                rest_obj = paginator1.page(page_number1)
            except PageNotAnInteger:
                rest_obj = paginator1.page(1)
            except EmptyPage:
                rest_obj = paginator1.page(paginator.num_pages)

            paginator2 = Paginator(meals, 6)
            page_number2 = request.GET.get('page2')
            try:
                meal_obj = paginator2.page(page_number2)
            except PageNotAnInteger:
                meal_obj = paginator2.page(1)
            except EmptyPage:
                meal_obj = paginator2.page(paginator.num_pages)

            context = {'query': query, 'categories': categories, 'restaurants': restaurants, 'meals': meals,
                       'users': users, 'items': items, 'rest_obj': rest_obj, 'meal_obj': meal_obj}
            return render(request, 'registration/search_results.html', context=context)

    def post(self, request, *args, **kwargs):
        query = request.POST.get('q')
        if query is not None:
            categories = RestaurantsMeal.objects.filter(Q(category__icontains=query))
            restaurants = Restaurant.objects.filter(Q(restaurant_name__icontains=query))
            meals = RestaurantsMeal.objects.filter(Q(meal_name__icontains=query))
            users = MyUser.objects.filter(Q(user__username__icontains=query) | Q(user__first_name__icontains=query) | Q(
                user__last_name__icontains=query) | Q(user__email__icontains=query))
            items = list(categories) + list(restaurants) + list(meals) + list(users)
            page_number = request.GET.get('page')
            paginator = Paginator(items, 10)
            try:
                page_obj = paginator.page(page_number)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            context = {'query': query, 'categories': categories, 'restaurants': restaurants, 'meals': meals,
                       'users': users, 'items': items, 'page_obj': page_obj}
            return render(request, 'registration/search_results.html', context=context)


"""def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid() and form.mail_is_unique():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})"""
