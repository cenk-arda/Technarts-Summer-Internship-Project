from django.urls import path, include
from restaurants import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('restaurants/', views.RestaurantListView.as_view(), name='restaurant_list'),
    path('restaurants/<int:restaurant_id>/', views.RestaurantView.as_view(), name='view_restaurant'),
    path('profile', views.EditProfileView.as_view(), name='edit_profile'),
    path('restaurants/<int:restaurant_id>/<int:meal_id>/', views.MealView.as_view(), name='view_meal'),
    path('restaurants/<int:restaurant_id>/<int:meal_id>/delete/<int:comment_id>', views.DeleteCommentView.as_view(),
         name='delete_review'),
    #path('add_avatar', views.ImageUploadView.as_view(), name='add_avatar'),
    path('user/<user_id>', views.UserView.as_view(), name="user_view"),
    path('favorites',views.FavoritesView.as_view(),name="favorites"),
]
