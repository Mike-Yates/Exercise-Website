from django.urls import path
from . import views

app_name = 'exercise'

# URL pattern to be used by the application
urlpatterns = [
    # path: /exercise/...
    path('landing/', views.route_to_landing_or_home, name="landing"),
    path('register/', views.register_user, name="register"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('firstlogin/', views.first_login, name='firstlogin'),
    path('home/', views.home, name='home'),
    path('blog/', views.blog_display, name='blog'),
    path('blog/submit', views.blog_post, name='submit'),
    path('sports/getsportsxp', views.read_sportsxp, name='getsportsxp'),
    path('sports/updatesportsxp', views.update_sportsxp, name='updatesportsxp'),
    path('sports/sortxp', views.sortxp, name='sortxp'),
    path('instructions/cardio', views.cardioView, name="cardio"),
    path('instructions/bodybuilding', views.bodyView, name="body"),
    path('instructions/sports', views.sportView, name="sport"),
    path('exercise_logging/', views.exercise_logging, name='exerciselogging'),
    path('bmi/', views.bmi_display, name="bmidisplay")  # page for bmi display

]
