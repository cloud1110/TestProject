# Create your views here.
#coding=utf-8\
from product.models import Product
from utils import render_response,PAGE_SIZE
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

@login_required
def product (request):
    keyword = request.GET.get('keyword','') 
    page_size = int(request.GET.get('page_size',PAGE_SIZE))
    if keyword:
        products = Product.objects.filter(en_name__istartswith=keyword)
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
def edit_add_product (request):
    form = ExamEntryForm(request.POST or None,initial={'pid':pid})
    if request.method == "POST":
        if form.is_valid():
            form.save(project_id=request.user.project.pk)
            return HttpResponseRedirect(reverse('examentry'))
    return render_response(request,'examentry_new.html',locals())


@check
@transaction.commit_on_success
def del_examentry(request,pid):
    examentry = get_object_or_404(ExamEntry,pk=pid)
    examentry.delete()
    sync(examentry)
    return HttpResponseRedirect(reverse('examentry'))