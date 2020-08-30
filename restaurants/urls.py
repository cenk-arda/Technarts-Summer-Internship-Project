from django.urls import path, include
from restaurants import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('restaurants/', views.RestaurantList.as_view(), name='restaurant_list'),
    path('restaurants/<int:restaurant_id>/', views.ViewRestaurant.as_view(), name='view_restaurant'),
    path('profile',views.edit_profile, name='edit_profile'),
    path('restaurants/<int:restaurant_id>/<int:meal_id>/',views.view_meal, name='view_meal'),
    path('restaurants/<int:restaurant_id>/<int:meal_id>/delete/<int:comment_id>',views.delete_review, name='delete_review')
]
