from django.conf.urls.defaults import patterns, include, url

from openchain.modules.views import index, chains, documents
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', index.main),
    url(r'^documents/all/$', documents.all),
    url(r'^documents/parse/$', documents.parse),
    url(r'^documents/new/(\d)/$', documents.new),
    url(r'^chains/addcheck/(\d)/(\d)/$', chains.addcheck),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
