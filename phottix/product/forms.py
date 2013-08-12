#coding=utf-8
from django import forms
from product.models import Product

class ProductForm (forms.Form):
    p_number = forms.CharField(label=u'编号',max_length=255)
    en_name = forms.CharField(label=u'英文名',max_length=255)
    tip = forms.CharField(label=u'信息',max_length = 255)
    cn_name = forms.CharField(label=u'中文名',max_length = 255)
    original_price = forms.CharField(label=u'原价')
    classification = forms.ChoiceField(label = u'分类')
    
    