from product.models import Product
from utils import render_response
from django.contrib.auth.decorators import login_required


def home (request):
    current_theme = "spacelab"
    if request.method == "POST":
        current_theme = request.POST.get('current_theme','spacelab')
        
    request.current_theme = current_theme
    request.session['current_theme'] = current_theme
    
    products = Product.objects.all()    
    productsnumber = len(products)
    
    return render_response(request, 'index.html', locals())