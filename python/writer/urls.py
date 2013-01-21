from django.conf.urls import patterns, include, url

from django.conf import settings

import nexus

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

nexus.autodiscover()

urlpatterns = patterns('',
    url(r'^nexus/', include(nexus.site.urls)),
    url(r'^$', 'artillery.views.home', name='home'),
    url(r'^write/$', 'artillery.views.write', name='write'),
    # Examples:
    # url(r'^$', 'writer.views.home', name='home'),
    # url(r'^writer/', include('writer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
