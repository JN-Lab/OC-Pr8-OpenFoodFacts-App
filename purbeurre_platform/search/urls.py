from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path('choice', views.choice, name="choice"),
    path('list/<element_type>/<info_id>', views.substitute, name="substitute"),
    path('product/<code>', views.product, name="product"),
    path('register', views.register, name="register"),
    path('login', views.log_in, name="log_in"),
    path('logout', views.log_out, name="log_out"),
    path('personal-account', views.personal, name="personal"),
    path('product-registered', views.product_registered, name="product_registered")
]