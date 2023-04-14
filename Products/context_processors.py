from category.models import category as c
from .models import Product
def menu_links(request):
    products = Product.objects.all()
    
    return dict(products=products)

