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
    path('blog/submit', views.blog_post, name='submit')
]
