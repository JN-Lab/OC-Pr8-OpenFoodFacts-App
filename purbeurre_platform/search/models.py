from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200)
    api_id = models.CharField(max_length=200)
    total_products = models.IntegerField(default=0)
    enough_good_nutriscore = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    ref = models.CharField(max_length=100)
    nutriscore = models.CharField(max_length=1)
    picture = models.URLField()
    had_been_registered = models.BooleanField(default=False)
    last_interaction = models.DateTimeField(default=timezone.now)
    categories = models.ManyToManyField(Category, related_name='products', blank=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='users', blank=True)

    def __str__(self):
        return self.user.username