# Generated by Django 2.0.6 on 2018-06-28 14:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('api_id', models.CharField(max_length=200)),
                ('total_product', models.IntegerField(default=0)),
                ('enough_good_nutriscore', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('ref', models.CharField(max_length=100)),
                ('nutriscore', models.CharField(max_length=1)),
                ('picture', models.URLField()),
                ('had_been_registered', models.BooleanField(default=False)),
                ('last_interaction', models.DateTimeField(default=django.utils.timezone.now)),
                ('categories', models.ManyToManyField(blank=True, related_name='products', to='search.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('products', models.ManyToManyField(blank=True, related_name='users', to='search.Product')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
