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
    owner = models.ForeignKey(User)
    mods = models.ManyToManyField(User, related_name='u+')
    is_nsfw = models.BooleanField(default=False)
    primary_genre = models.ForeignKey(Genre)
    genres = models.ManyToManyField(Genre, related_name='genre+')


class Story(models.Model):
    (
            ORIGINAL,
            APPROVED,
            SIDE,
            FANFICTION,
    ) = range(4)

    title = models.CharField(max_length=100)
    tagline = models.CharField(max_length=160)
    summary = models.TextField(blank=True)

    author = models.ForeignKey(User)
    editors = models.ManyToManyField(User, related_name='editor+')
    canon = models.ForeignKey(Canon)

    # For if a story is considered officially part of a canon or not.
    classification = models.PositiveIntegerField(choices=(
        (ORIGINAL, 'original work'),
        (APPROVED, 'approved work'),
        (SIDE, 'side story'),
        (FANFICTION, 'fanmade'),)
    )


class Chapter(models.Model):
    title = models.CharField(max_length=100)
    story = models.ForeignKey(Story)
    order = models.PositiveIntegerField()
    content = models.TextField()

    class Meta:
        unique_together = ('story', 'order')
