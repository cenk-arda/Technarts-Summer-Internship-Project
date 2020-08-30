from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('home/', views.Home.as_view(), name='home'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='registration/login.html') , name='login'), ## default template name was registration/login.html, I wanted to change this.
    path('accounts/logout/',auth_views.LogoutView.as_view(template_name='registration/mainpage.html'), name='loggedout'),
    path('accounts/password_reset/',auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html',email_template_name='registration/email_template.html',subject_template_name='registration/subject_template.txt',), name = 'password_reset'),
    path('accounts/password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name = 'password_reset_done'),
    path('accounts/reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_complete.html'), name = 'reset_done'),
    path('accounts/reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/', include('django.contrib.auth.urls')),


]
##auth_views.LoginView.as_view(template_name='registration/login.html')
""" Last line above includes the following URL patterns:
accounts/login/ [name='login']
accounts/logout/ [name='logout']
accounts/password_change/ [name='password_change']
accounts/password_change/done/ [name='password_change_done']
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']"""