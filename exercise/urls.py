from django.urls import path
from . import views

app_name = 'exercise'

# URL pattern to be used by the polls
urlpatterns = [
    # path: /exercise/
    path('', views.IndexView.as_view(), name='index'),
]
