from django.conf.urls.defaults import patterns, include, url

from openchain.modules.views import index, alldocs, getforms
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', index.main),
    url(r'^alldocs/$', alldocs.main),
    url(r'^getforms/$', getforms.main),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
