from django.urls import path
from . import views

app_name = 'exercise'

# URL pattern to be used by the application - Not yet implemented since has not started app -
urlpatterns = [
    # path: /exercise/
    path('register/', views.register_page, name="register"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('home/', views.home, name='home'),
]
