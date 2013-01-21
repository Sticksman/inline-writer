from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    description = models.TextField(blank=True)

class Canon(models.Model):
    admins = models.ManyToManyField(User)
    

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
    canon = models.ForeignKey(Canon)
    

    author = models.ForeignKey(User)
    editors = models.ManyToManyField(User, related_name='editor+', null=True)

    # For if a story is considered officially part of a canon or not.
    classification = models.PositiveIntegerField(choices=(
        (ORIGINAL, 'original work'),
        (APPROVED, 'approved work'),
        (SIDE, 'side story'),
        (FANFICTION, 'fanmade'),)
    )

    related_stories = models.ManyToManyField('Story', related_name='story+', null=True)
    created_on = models.DateField(auto_now_add=True)
    modified_on = models.DateField(auto_now=True)

class Subscription(models.Model):
    user = models.ForeignKey(User)
    canon = models.ForeignKey(Canon)

class StoryArt(models.Model):
    story = models.ForeignKey(Story, blank=True)
    art = models.ImageField(upload_to='storyart/%Y-%m-%d/')
    created_on = models.DateField(auto_now_add=True)
    modified_on = models.DateField(auto_now=True)


class Chapter(models.Model):
    title = models.CharField(max_length=100)
    story = models.ForeignKey(Story)
    order = models.PositiveIntegerField()
    content = models.TextField()
    created_on = models.DateField(auto_now_add=True)
    modified_on = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('story', 'order')
