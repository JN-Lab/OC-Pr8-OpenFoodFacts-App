from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path('choice', views.choice, name="choice"),
    path('list/<element_type>/<info_id>', views.substitute, name="substitute"),
    path('product/<code>', views.product, name="product"),
]