from django.urls import path, include
from restaurants import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('restaurants/', views.RestaurantList.as_view(), name='restaurant_list'),
    path('restaurants/<int:restaurant_id>/', views.ViewRestaurant.as_view(), name='view_restaurant'),
    path('profile',views.EditProfile.as_view(), name='edit_profile'),
    path('restaurants/<int:restaurant_id>/<int:meal_id>/',views.ViewMeal.as_view(), name='view_meal'),
    path('restaurants/<int:restaurant_id>/<int:meal_id>/delete/<int:comment_id>',views.DeleteReview.as_view(), name='delete_review')
]
