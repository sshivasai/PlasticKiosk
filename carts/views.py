from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from Products.models import Product
from accounts.models import UserProfile
# Create your views here.
from django.http import HttpResponse

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

@login_required(login_url='login')
def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    if current_user.is_authenticated:
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user).first()
            if cart_item.product == product:
                cart_item.quantity+=1
                cart_item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                item.save()
        else:
            item = CartItem.objects.create(product=product, quantity=1, user=current_user)
            item.save()
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user).first()
            if cart_item.product == product:
                cart_item.quantity+=1
                cart_item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                item.save()
        else:
            item = CartItem.objects.create(product=product, quantity=1, user=current_user)
            item.save()
    cart_item = CartItem.objects.filter(product=product, user=current_user).first()
    cat_id = cart_item.product.price.category.cat_id
    
    return redirect('cart')

def remove_cart(request, product_id, cart_item_id):

    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None):
    cat_id = None
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            cart_item = CartItem.objects.filter(user=request.user, is_active=True).first()
            if cart_item:
                cat_id = int(cart_item.product.price.category.cat_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            cart_item = CartItem.objects.filter(cart=cart, is_active=True).first()
            if cart_item.product:
                cat_id = int(cart_item.productprice.category.cat_id)
        for cart_item in cart_items:
            total += (cart_item.product.price.price_per_pound * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore
    
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
        'cat_id':cat_id,
    }
    return render(request, 'Products/cart.html', context)




@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price.price_per_pound * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore
    cart_items_first = CartItem.objects.filter(user=request.user, is_active=True).first()
    cat_id = cart_items_first.product.price.category.cat_id
    userprofile = UserProfile.objects.filter(user = request.user).first()
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
        'cat_id':cat_id,
        'userprofile':userprofile,
    }
    return render(request, 'Products/checkout.html', context)
