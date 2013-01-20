# Create your views here.
from django import shortcuts
from django import template

def home(request):
    return shortcuts.render_to_response('base.html',{})
    pass
