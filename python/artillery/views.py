# Create your views here.
from django import shortcuts
from django import template
from django.contrib.auth.decorators import login_required
from ext.token import decrypt_string

from artillery import models
import api

def home(request):
    stories = models.Story.objects.all()
    return shortcuts.render_to_response('artillery/base.html',{})
    pass

@login_required
def subscriptions(request):
    pass

def write(request):
    return shortcuts.render_to_response('artillery/write.html', {})


#API handlers

@login_required
def handle_subscriptions(request, subscription_token=None):
    if request.method == "POST":
        return post_subscription(request)
    if request.method == "GET":
        if subscription_token:
            return get_subscription(request, subscription_token)
        return get_subscriptions(request)
    if request.method == "DELETE":
        return delete_subscriptions(request, subscription_token)

def post_subscription(request):
    canon_id = decrypt_string(request.POST.get("canon_token"))
    data = api.create_subscription(canon_id, request.user.id)


