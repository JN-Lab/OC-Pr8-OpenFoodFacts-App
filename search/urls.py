from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path('choice', views.choice, name="choice"),
    path('list/<element_type>/<info_id>', views.substitute, name="substitute"),
    path('product/<code>', views.product, name="product"),
    path('personal-account', views.personal, name="personal"),
    path('product-registered', views.product_registered, name="product_registered"),
    path('save-treatment/<code>', views.save_treatment, name="save_treatment"),
    path('delete-treatment/<code>', views.delete_treatment, name="delete_treatment"),
]