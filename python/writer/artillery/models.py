from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    description = models.TextField(blank=True)


class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_on = models.DateField()
    modified_on = models.DateField()


class Canon(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(User)
    is_nsfw = models.BooleanField(default=False)
    primary_genre = models.ForeignKey(Genre)
    genres = models.ManyToManyField(Genre, related_name='genre+')
