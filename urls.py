from django.conf.urls.defaults import patterns, include, url

from modules.views import index, chains, documents, taglink, support, login, perms
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index.main),
    url(r'^documents/all/$', documents.all),
    url(r'^documents/parse/$', documents.parse),
    url(r'^documents/new/(\d+)/$', documents.new), # id_doc, number of master == 0
    url(r'^documents/new/(\d+)/(\d+)/$', documents.new), # id_doc, number of master or 0
    url(r'^documents/new/$', documents.new), # change id_doc for create
    url(r'^documents/show/$', documents.show), # id_doc, number of master == 0
    url(r'^documents/edit/$', documents.show), # id_doc, number of master == 0
    url(r'^documents/show/(\d+)/$', documents.show), # id_doc, number of master == 0
    url(r'^documents/edit/(\d+)/$', documents.edit), # id_doc, number of master == 0
    url(r'^documents/held/(\d+)/$', documents.held), # id_doc, number of master == 0
    url(r'^documents/odf/(\d+)/$', documents.odf), # id_doc, number of master == 0
    url(r'^documents/perm_error/$', documents.perm_error),
    url(r'^chains/addcheck/(\d+)/(\d+)/$', chains.addcheck),
    url(r'^chains/add/$', chains.add),
    url(r'^chains/need/$', chains.need),
    url(r'^tags/links/$', taglink.links),
    url(r'^tags/show/$', taglink.show),
    url(r'^support/$', support.main),
    url(r'^login/$', login.main),
    url(r'^perms/user/$', perms.user),
    url(r'^perms/user/(.+)/(\d+)/$', perms.user),
    url(r'^perms/group/$', perms.group),
    url(r'^perms/group/(.+)/(\d+)/$', perms.group),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
