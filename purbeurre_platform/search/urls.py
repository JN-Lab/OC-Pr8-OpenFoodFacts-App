from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path('choice', views.choice, name="choice"),
    path('list/<type>/<slug:type_name>', views.list, name="list"),
]