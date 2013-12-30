#coding=utf-8
from django.db import models
from utils import auto_code
from core.manager import FakeDeleteManager,FakeDeleteModel

class Product(FakeDeleteModel):
	Product_Classification = (
		(0,u'无线遥控'),
		(1,u'有线遥控'),
		(2,u'电池盒'),
		(3,u'电池'),
		(4,u'闪光灯配件'),
		(5,u'影楼配件'),
		(6,u'其他配件')
	)
	p_number = models.CharField(max_length=200)
	en_name = models.CharField(max_length=200)
	tip = models.CharField(max_length=200)
	cn_name = models.CharField(max_length=200)
	original_price = models.CharField(max_length=50)
	classification = models.IntegerField(choices = Product_Classification)
	
	objects = FakeDeleteManager()

	def __init__(self, *args, **kargs):
		super(Product, self).__init__(*args, **kargs)
		if not getattr(self, 'code',  None):
			self.code = auto_code()


	def __unicode__(self):
		return self.name
	
