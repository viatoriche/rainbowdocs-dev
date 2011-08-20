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
    url(r'^documents/new/(\d)/$', documents.new), # id_doc, number of master == 0
    url(r'^documents/new/(\d)/(\d)/$', documents.new), # id_doc, number of master or 0
    url(r'^documents/new/$', documents.new), # change id_doc for create
    url(r'^documents/show/$', documents.show), # id_doc, number of master == 0
    url(r'^documents/edit/$', documents.show), # id_doc, number of master == 0
    url(r'^documents/show/(\d)/$', documents.show), # id_doc, number of master == 0
    url(r'^documents/edit/(\d)/$', documents.edit), # id_doc, number of master == 0
    url(r'^documents/held/(\d)/$', documents.held), # id_doc, number of master == 0
    url(r'^documents/odt/(\d)/$', documents.odt), # id_doc, number of master == 0
    url(r'^chains/addcheck/(\d)/(\d)/$', chains.addcheck),
    url(r'^chains/need/$', chains.need),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
