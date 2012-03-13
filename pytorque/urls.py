from django.conf.urls.defaults import *

urlpatterns = patterns('pytorque.views',
    (r'^$', 'central_dispatch_view'),
    (r'^login/$', 'login'),
    (r'^logout/$', 'logout'),

#    (r'^$', 'central_dispatch_view'),
    (r'^user/(?P<username>\w{0,50})/$', 'index'),
)
  