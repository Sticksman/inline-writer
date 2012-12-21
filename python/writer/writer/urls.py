from django.conf.urls import patterns, include, url

import nexus

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

nexus.autodiscover()

urlpatterns = patterns('',
    url(r'^nexus/', include(nexus.site.urls),
    # Examples:
    # url(r'^$', 'writer.views.home', name='home'),
    # url(r'^writer/', include('writer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
