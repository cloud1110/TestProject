  

from django.contrib.auth.models import Permission
from django.db.models.signals import post_syncdb
from django.contrib.contenttypes.models import ContentType
from product import models

def __initial_permission(sender, **kwargs):
    print 'create predefine permssion'
    Permission.objects.all().delete()
    content_type = ContentType.objects.get(model='product')
    Permission.objects.get_or_create(name='access_product', content_type=content_type, codename='access_product')

post_syncdb.connect(__initial_permission, sender=models)
