from django.urls import path
from . import views

app_name = 'exercise'

# URL pattern to be used by the application - Not yet implemented since has not started app -
urlpatterns = [
    # path: /exercise/
    # path('', views.IndexView.as_view(), name='index'),
    path('blog/', views.blogDisplay, name='blog'),
    path('blog/submit', views.thot, name='submit')
]
