from django.shortcuts import render, HttpResponse
from carts.models import CartItem
from carts.views import _cart_id
from category.models import category
# Create your views here.
from orders.models import  OrderProduct
from .models import Product
def productbycategory(request,name):
    temp = Product.objects.all()
    cat_id = category.objects.filter(name=name).first().cat_id
    
    products = []
    for x in temp:
        if str(x.price.category.name) == name:
            products.append(x)
    
    context = {
        'products':products,
        'cat_id': cat_id,
    }
    print(cat_id)
    return render(request,'Products/products.html',context)

def productbyname(request,product_name):
    try:
        current_user = request.user
        product = Product.objects.all().filter(product_name = product_name)
        product_first = Product.objects.all().filter(product_name = product_name).first()
        if request.user.is_authenticated:
            in_cart = CartItem.objects.filter(product=product_first.id, user=current_user).exists()
        else:
            in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product_first.id).exists()
        print(in_cart)
        cat_id = int(product_first.price.category.cat_id)
    except Exception as e:
        raise e

    #print(in_cart)
    context = {
        'product': product,
        'in_cart'       : in_cart,
        'cat_id':cat_id
    }
    
    return render(request, 'Products/products_details.html', context)
    