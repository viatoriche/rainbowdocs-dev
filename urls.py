"""ALL URLS"""

from django.conf.urls.defaults import patterns, include, url

from modules.views import index, chains, documents
from modules.views import taglink, support, login, perms
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index.main),
    # Tested
    url(r'^documents/all/$', documents.all),
    # Tested
    url(r'^documents/parse/$', documents.parse),
    # Tested
    url(r'^documents/new/(\d+)/$', documents.new),
    # Tested
    url(r'^documents/new/(\d+)/(\d+)/$', documents.new),
    # Tested
    url(r'^documents/new/$', documents.new),
    # Tested
    url(r'^documents/show/$', documents.show),
    # Tested
    url(r'^documents/edit/$', documents.show),
    # Tested
    url(r'^documents/show/(\d+)/$', documents.show),
    # Tested
    url(r'^documents/edit/(\d+)/$', documents.edit),
    # Tested
    url(r'^documents/held/(\d+)/$', documents.held),
    # Tested
    url(r'^documents/odf/(\d+)/$', documents.odf),
    # Tested
    url(r'^documents/perm_error/$', documents.perm_error),
    # Tested
    url(r'^chains/addcheck/(\d+)/(\d+)/$', chains.addcheck),
    # Tested
    url(r'^chains/add/$', chains.add),
    # Tested
    url(r'^chains/need/$', chains.need),
    # Tested
    url(r'^tags/links/$', taglink.links),
    # Tested
    url(r'^tags/show/$', taglink.show),
    # Tested
    url(r'^support/$', support.main),
    # Tested
    url(r'^login/$', login.main),
    # Tested
    url(r'^perms/user/$', perms.user),
    url(r'^perms/user/(.+)/(\d+)/$', perms.user),
    # Tested
    url(r'^perms/group/$', perms.group),
    url(r'^perms/group/(.+)/(\d+)/$', perms.group),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
