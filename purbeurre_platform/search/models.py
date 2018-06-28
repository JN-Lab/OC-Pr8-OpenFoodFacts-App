from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneFlied(User)

class Product(models.Model):
    name = models.CharField(max_length=200)
    ref = models.CharField(max_length=100)
    nutriscore = models.CharField(max_length=1)
    picture = models.URLField()
    had_been_registered = models.BooleanField(default=False)
    last_interaction = models.DateTimeField(default=timezone.now)

class Category(models.Model):
    name = models.CharField(max_length=200)
    api_id = models.CharField(max_length=200)
    total_product = models.IntegerField(default=0)
    enough_good_nutriscore = models.BooleanField(default=False)

