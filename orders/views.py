from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct, stores as s, category
from accounts.models import UserProfile
import json
from Products.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.db.models import Q

def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    # Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        if orderproduct.order.order_type.cat_id == 1: #for household
            orderproduct.payment = None
        else:
            orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price.price_per_pound
        orderproduct.ordered = True
        orderproduct.save()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.save()

        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        if product.price.category.cat_id == 1: # for household
            product.current_stock += item.quantity
        else:
            product.current_stock -= item.quantity
        product.save()

    # Clear cart
    CartItem.objects.filter(user=request.user).delete()

    # Send order recieved email to customer
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_recieved_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    #print(to_email)
    from_email = "plastickiosk@gmail.com"
    
    send_email = EmailMessage(subject=mail_subject,body= message,from_email = from_email, to=[to_email])
    send_email.send()

    # Send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)

def place_order(request, total=0, quantity=0,):
    pickup_location=None
    current_user = request.user

    # If the cart count is less than or equal to 0, then redirect back to home
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('home')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price.price_per_pound * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.pickup_location = form.cleaned_data['pickup_location']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            print(data.pickup_location)
            if form.cleaned_data['pickup_location'] == "None" :
                data.order_type = category.objects.filter(cat_id = 1).first() #1 for household
            else:
                pickup_location = s.objects.all().filter( Q(name__icontains=data.pickup_location)).first()
                data.pickup_location = str(pickup_location.name) + ","+ str(pickup_location.address)
                data.order_type = category.objects.filter(cat_id = 2).first() #2 for retailer
            
            
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            
            cat_id = data.order_type.cat_id
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
                'pickup_location' : pickup_location,
                'cat_id':cat_id,
                
                
            }
            return render(request, 'orders/payments.html', context)
    else:
        return redirect('checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
    
        subtotal = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        temp = OrderProduct.objects.filter(order_id=order.id).first()
        if temp.order.order_type.cat_id == 2: # for retailer 
            payment = Payment.objects.get(payment_id=transID)
        else:
            payment = "Cash"

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
            'cat_id' : 2
            
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')


def order_complete_house(request,order_number):
    order = Order.objects.get(order_number=order_number)
    order.is_ordered = True
    ordered_products = OrderProduct.objects.filter(order_id=order.id)
    order.save()
    # Send order recieved email to customer
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_recieved_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    #print(to_email)
    from_email = "plastickiosk@gmail.com"
    
    send_email = EmailMessage(subject=mail_subject,body= message,from_email = from_email, to=[to_email])
    send_email.send()
    context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': None,
            'payment': "Cash",
            'subtotal': order.order_total - order.tax,
            'cat_id' : 1
            
        }
    return render(request, 'orders/order_complete.html',context)


def order_complete_small(request,order_number):
    order = Order.objects.get(order_number=order_number)

    order.is_ordered = True
    ordered_products = OrderProduct.objects.filter(order_id=order.id)
    order.save()
    # Send order recieved email to customer
    mail_subject = 'Thank you for your order!'
    message = render_to_string('orders/order_recieved_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    #print(to_email)
    from_email = "plastickiosk@gmail.com"
    
    send_email = EmailMessage(subject=mail_subject,body= message,from_email = from_email, to=[to_email])
    send_email.send()
    context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': None,
            'payment': "Cash",
            'subtotal': order.order_total - order.tax,
            'cat_id' : 2,
            'status': "Order Placed"
            
        }
    return render(request, 'orders/order_complete.html',context)