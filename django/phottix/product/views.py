# Create your views here.
#coding=utf-8\
from product.models import Product
from product.forms import ProductForm
from utils import render_response,PAGE_SIZE
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage


def product (request):
    keyword = request.GET.get('keyword','') 
    page_size = int(request.GET.get('page_size',PAGE_SIZE))
    if keyword:
        products = Product.objects.filter(Q(en_name__icontains=keyword)|Q(cn_name__icontains=keyword))
    else:
        products = Product.objects.all()
    total = len(products)
    paginator = Paginator(products, int(page_size))
    page = request.GET.get('page')
    
    try:
        product_list = paginator.page(page)
    except PageNotAnInteger:
        product_list = paginator.page(1)
    except EmptyPage:
        product_list = paginator.page(paginator.num_pages)
        
    return render_response(request,'product/index.html',locals())

@login_required
def edit_add_product (request,pid = None):
    form = ProductForm(request.POST or None,initial={'pid':pid})
    if request.method == "POST":
        if form.is_valid():
            form.save(project_id=request.user.project.pk)
            return HttpResponseRedirect(reverse('product'))
    return render_response(request,'product_new.html',locals())


@login_required
def del_product(request,pid):
    product = get_object_or_404(Product,pk=pid)
    product.delete()
    return HttpResponseRedirect(reverse('product'))

