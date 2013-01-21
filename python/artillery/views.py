# Create your views here.
from django import shortcuts
from django import template

from artillery import models

def home(request):
    stories = models.Story.objects.all()
    return shortcuts.render_to_response('base.html',{})
