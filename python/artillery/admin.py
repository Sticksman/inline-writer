from django.contrib import admin
from artillery import models

admin.site.register(models.User)

admin.site.register(models.Story)
