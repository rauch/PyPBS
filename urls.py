from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic.simple import redirect_to
import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', redirect_to, {'url': '/pytorque/'}),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),

    url(r'^pytorque/', include('pytorque.urls')),
)
