from django import template

from django.conf import settings

register = template.Library()

@register.simple_tag(takes_context=True)
def static_url(context, location):
    location = unicode(location)
    url = settings.MEDIA_URL
    if not url.endswith("/"):
        url += "/"
    if location.startswith("/"):
        location = location[1:]
    return url + location
