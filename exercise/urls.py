from django.urls import path
from . import views

app_name = 'exercise'

# URL pattern to be used by the application - Not yet implemented since has not started app -
urlpatterns = [
    # path: /exercise/
    # path('', views.IndexView.as_view(), name='index'),
    path('schedule', views.runningView.as_view(), name="cardio"),
    path('schedule2', views.bigView.as_view(), name="big"),
    path('schedule3', views.sportView.as_view(), name="sport"),
    path('fakeHome/', views.fakeHome.as_view(),name='fake'),

    path('blog/', views.blogDisplay, name='blog'),
    path('blog/submit', views.thot, name='submit')
]
