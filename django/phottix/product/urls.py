from django.conf.urls import patterns, url


urlpatterns = patterns('product.views',
                       
    url(r'^$', 'product',name = 'product'),
    url(r'^edit/$', 'edit_add_product',name = 'edit_product'),
    url(r'^add/$', 'edit_add_product',name = 'add_product'),
    url(r'^del/$', 'del_product',name = 'del_product'),
)