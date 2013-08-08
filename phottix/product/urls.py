from django.conf.urls import patterns, url


urlpatterns = patterns('product.views',
                       
    url(r'^product/$', 'product',name = 'products-list'),
)