from django.conf.urls import patterns, include, url
import django.contrib.auth.views as django_auth

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^login/$', django_auth.login, name='login'),
    # url(r'^$', 'phottix.views.home', name='home'),
    # url(r'^phottix/', include('phottix.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^product/', include('product.urls')),
)
