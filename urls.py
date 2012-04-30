from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import settings

admin.autodiscover()

urlpatterns = patterns('',
    #    url(r'^$', redirect_to, {'url': '/pytorque/'}),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/media/images/favicon.ico'}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True})
    ,

    #    url(r'^pytorque/', include('pytorque.urls')),


    (r'^$', 'pytorque.views.central_dispatch_view'),
    (r'^browse$', 'pytorque.views.central_dispatch_view'),
    (r'^monitor$', 'pytorque.views.central_dispatch_view'),
    (r'^submit$', 'pytorque.views.central_dispatch_view'),
    (r'^stat$', 'pytorque.views.central_dispatch_view'),

    (r'^login/$', 'pytorque.views.login'),
    (r'^logout/$', 'pytorque.views.logout'),

    (r'^user/(?P<username>\w{0,50})/$', 'pytorque.views.index'),
    (r'^user/(?P<username>\w{0,50})/browse$', 'pytorque.views.browse'),
    (r'^user/(?P<username>\w{0,50})/browse/get_children$', 'pytorque.views.get_children'),
    (r'^user/(?P<username>\w{0,50})/browse/upload$', 'pytorque.views.fileUpload'),
    (r'^user/(?P<username>\w{0,50})/browse/download$', 'pytorque.views.fileDownload'),
    (r'^user/(?P<username>\w{0,50})/browse/remove$', 'pytorque.views.fileRemove'),
    (r'^user/(?P<username>\w{0,50})/monitor$', 'pytorque.views.monitor'),
    (r'^user/(?P<username>\w{0,50})/monitor/get_jobs$', 'pytorque.views.get_jobs'),
    (r'^user/(?P<username>\w{0,50})/submit$', 'pytorque.views.submit'),
    (r'^user/(?P<username>\w{0,50})/stat$', 'pytorque.views.stat'),
)
