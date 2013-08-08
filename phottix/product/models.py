from django.db import models

# Create your models here.
class Product(models.Model):
	en_name = models.CharField(max_length=200)
	tip = models.CharField(max_length=200)
	cn_name = models.CharField(max_length=200)
	original_price = models.FloatField(default=0)
