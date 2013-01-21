from django.db.models.query import QuerySet
from django.conf import settings
from django.http import HttpResponseRedirect

def ssl_required(view_func):
    return view_func
    # TODO Fix this
    def _checkssl(request, *args, **kwargs):
        if not settings.DEBUG and not request.is_secure():
            if hasattr(settings, 'SSL_DOMAIN'):
                url_str = urlparse.urljoin(
                    settings.SSL_DOMAIN,
                    request.get_full_path()
                )
            else:
                url_str = request.build_absolute_uri()
            url_str = url_str.replace('http://', 'https://')
            return HttpResponseRedirect(url_str)

        return view_func(request, *args, **kwargs)
    return _checkssl

def repeatable(func):
    def decked(repeator, *args, **kwargs):
        is_qs = isinstance(repeator, QuerySet)
        is_list = isinstance(repeator, list)
        is_tuple = isinstance(repeator, tuple)
        if not (is_qs or is_list or is_tuple):
            return func([repeator], *args, **kwargs)[0]
        return func(repeator, *args, **kwargs)
    return decked
