from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOne(User, primary_key=True)
    description = models.CharField(max_length=140)

