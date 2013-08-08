# Create your views here.
#coding=utf-8\
from product.models import Product
from utils import render_response,PAGE_SIZE
from django.contrib.auth.decorators import login_required

@login_required
def product (request):
    keyword = request.GET.get('keyword','')
    page_size = int(request.GET.get('page_size',PAGE_SIZE))
    if keyword:
        products = Product.objects.filter(en_name__istartswith=keyword)
    else:
        products = Product.objects.all()
    return render_response(request,'index.html',locals())