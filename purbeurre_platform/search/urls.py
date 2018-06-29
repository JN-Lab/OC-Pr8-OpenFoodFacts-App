from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path('search/choice', views.choice, name="choice"),
]