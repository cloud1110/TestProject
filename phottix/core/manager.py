from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver



class DonotDeleteException(BaseException):
    pass


class FakeDeleteManager(models.Manager):
    def get_query_set(self):
        return super(FakeDeleteManager, self).get_query_set().filter(is_deleted=False)


class FakeDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)

    objects = FakeDeleteManager()

    class Meta:
        abstract = True

    def delete(self):
        self.is_deleted = True
        self.save()

#@receiver(pre_delete, sender=FakeDeleteModel)
def _fake_delete(sender, instance, **kwargs):
    if isinstance(instance, FakeDeleteModel):
        #instance.is_deleted = True
        #instance.save()
        # an ugly hack, don't delete model by queryset.delete()
        raise DonotDeleteException('Do not delete') 
    else:
        pass

pre_delete.connect(_fake_delete)

class AutoTimeModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
