from django.shortcuts import render, redirect
from django.http import HttpResponse
from carts.models import CartItem
from .forms import OrderForm
from .models import Order, OrderProduct
import datetime
from .models import Payment
from .models import Order
from datetime import datetime as dt
import random
from store.models import Product
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from accounts.models import Account, UserProfile, AddAddress, AddState, AddEmailAddress
from carts.models import Cart
from carts.views import _cart_item
from django.contrib import messages, auth
# Create your views here.



def payment(request):
    return render(request, 'orders/payment.html')

def makePayment(request, order_number, email):
    if request.user.is_authenticated:
        user =request.user
        order = Order.objects.get(user=user, is_ordered=False, order_number=order_number)
        user_for_id = user.email.split('@')[0]
    else:
        order = Order.objects.get(email=email, is_ordered=False, order_number=order_number)
        user_for_id = email.split('@')[0]

    
    now = dt.now()
    current_time1 = now.strftime("%H%M%S")
    current_time2= now.strftime("%S%M%H")
    ran = random.randint(0, 2)
    
    if(ran==1):
        payment_id=current_time1 + user_for_id
    else:
        payment_id=current_time2 + user_for_id

    grand_total= order.order_total
    if request.user.is_authenticated:
        payment =Payment(
            user=user,
            payment_id=payment_id,
            payment_method="database",
            amount_paid=grand_total,
            status="COMPLETED"
        )
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        payment =Payment(
            payment_id=payment_id,
            payment_method="database",
            amount_paid=grand_total,
            status="COMPLETED"
        )
        cart = Cart.objects.get(cart_id= _cart_item(request))
        cart_items = CartItem.objects.filter(cart =cart, is_active=True)
        

    payment.save()

    order.payment=payment
    order.is_ordered =True
    order.save()


    
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        if request.user.is_authenticated:
            orderproduct.user_id = request.user.id
        
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered =True
        orderproduct.save()

        cart_item = CartItem.objects.get(id = item.id)
        product_variation = cart_item.variation.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variation.set(product_variation)
        orderproduct.save()

        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    yr = int(datetime.date.today().strftime('%Y'))
    dy = int(datetime.date.today().strftime('%d'))
    mt = int(datetime.date.today().strftime('%m'))
    d =datetime.date(yr,mt,dy)
    current_date = d.strftime("%Y%m%d")
    #######################################Authentication Part Start#################################
    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user).delete()
        
        payment = Payment.objects.get(user=request.user,payment_id=payment_id)
        order = Order.objects.get(user=request.user, order_number=order_number, is_ordered=True)
        orderproduct = OrderProduct.objects.filter(user=request.user, payment=payment, order=order)
        total = 0
        for orderP in orderproduct:
            total+= orderP.quantity * orderP.product_price

        mail_subject = 'Thank you for your order'
        message = render_to_string('orders/order_recieved_email.html', {
                    'user':request.user,
                    'orderproduct':orderproduct,
                    'order_number':order_number,
                    'payment_id':payment_id,
                    'current_date':current_date,
                    'order':order,
                    'total':total,
                    'for':'user'

                })
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

        mail_subject = 'Got New Order'
        message = render_to_string('orders/order_recieved_email.html', {
                    'user':request.user,
                    'orderproduct':orderproduct,
                    'order_number':order_number,
                    'payment_id':payment_id,
                    'current_date':current_date,
                    'order':order,
                    'total':total,
                    'for':'admin'

                })
        
        take_email = Order.objects.get(order_number = order_number, is_ordered=True)
        state_name = take_email.state.state
        email_add = AddEmailAddress.objects.get(state__state =  state_name)
        to_email = email_add.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

        to_email = 'aacs807@gmail.com'
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

    #######################################Authentication Part Over#################################



    else:
        cart = Cart.objects.get(cart_id= _cart_item(request))
        CartItem.objects.filter(cart =cart, is_active=True).delete()
        
        payment = Payment.objects.get(payment_id=payment_id)
        order = Order.objects.get(order_number=order_number, email=email ,is_ordered=True)
        orderproduct = OrderProduct.objects.filter(payment=payment, order=order)
        total = 0
        for orderP in orderproduct:
            total+= orderP.quantity * orderP.product_price

        mail_subject = 'Thank you for your order'
        message = render_to_string('orders/order_recieved_email.html', {
                    'user':{'first_name': email},
                    'orderproduct':orderproduct,
                    'order_number':order_number,
                    'payment_id':payment_id,
                    'current_date':current_date,
                    'order':order,
                    'total':total,
                    'for':'user'
                })
        to_email= email
        send_email = EmailMessage(mail_subject, message, to=[to_email, 'mainEmail@'])
        send_email.send()


        mail_subject = 'Got new Order'
        message = render_to_string('orders/order_recieved_email.html', {
                    'user':{'first_name': email},
                    'orderproduct':orderproduct,
                    'order_number':order_number,
                    'payment_id':payment_id,
                    'current_date':current_date,
                    'order':order,
                    'total':total,
                    'for':'admin'
                })
        take_email = Order.objects.get(order_number = order_number, is_ordered=True)
        state_name = take_email.state.state
        email_add = AddEmailAddress.objects.get(state__state =  state_name)
        to_email = email_add.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

        to_email = 'aacs807@gmail.com'
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

    context={
        'orderproduct':orderproduct,
        'order_number':order_number,
        'payment_id':payment_id,
        'current_date':current_date,
        'order':order,
        'total':total,
    }
    return render(request, 'orders/order_complete.html', context)
    
########################################################################################### Through ADD TO CART END ########################################################


########################################################################################### Through BUY NOW  ########################################################

def buy_makePayment(request, order_number, email):
    if request.user.is_authenticated:
        user =request.user
        order = Order.objects.get(user=user, is_ordered=False, order_number=order_number)
        user_for_id = user.email.split('@')[0]
    else:
        order = Order.objects.get(email=email, is_ordered=False, order_number=order_number)
        user_for_id = email.split('@')[0]

    
    now = dt.now()
    current_time1 = now.strftime("%H%M%S")
    current_time2= now.strftime("%S%M%H")
    ran = random.randint(0, 2)
    
    if(ran==1):
        payment_id=current_time1 + user_for_id
    else:
        payment_id=current_time2 + user_for_id

    grand_total= order.order_total
    if request.user.is_authenticated:
        payment =Payment(
            user=user,
            payment_id=payment_id,
            payment_method="database",
            amount_paid=grand_total,
            status="COMPLETED"
        )
        cart_item = CartItem.objects.filter(user=request.user)
        cart_items=None
        for carts in cart_item:
            cart_items=carts
    else:
        payment =Payment(
            payment_id=payment_id,
            payment_method="database",
            amount_paid=grand_total,
            status="COMPLETED"
        )
        cart = Cart.objects.get(cart_id= _cart_item(request))
        cart_item = CartItem.objects.filter(cart =cart, is_active=True)
        cart_items=None
        for carts in cart_item:
            cart_items=carts

    payment.save()

    order.payment=payment
    order.is_ordered =True
    order.save()
    orderproduct = OrderProduct()
    orderproduct.order_id = order.id
    orderproduct.payment = payment
    if request.user.is_authenticated:
        orderproduct.user_id = request.user.id
        
    orderproduct.product_id = cart_items.product_id
    orderproduct.quantity = 1
    orderproduct.product_price = cart_items.product.price
    orderproduct.ordered =True
    orderproduct.save()

    cart_item = CartItem.objects.get(id = cart_items.id)
    product_variation = cart_item.variation.all()
    orderproduct = OrderProduct.objects.get(id=orderproduct.id)
    orderproduct.variation.set(product_variation)
    orderproduct.save()

    product = Product.objects.get(id=cart_items.product_id)
    product.stock -= cart_items.quantity
    product.save()

    yr = int(datetime.date.today().strftime('%Y'))
    dy = int(datetime.date.today().strftime('%d'))
    mt = int(datetime.date.today().strftime('%m'))
    d =datetime.date(yr,mt,dy)
    current_date = d.strftime("%Y%m%d")

    if request.user.is_authenticated:
        cart_item = CartItem.objects.filter(user=request.user)
        a=None
        for carts in cart_item:
            a= carts
        a.delete()

        payment = Payment.objects.get(user=request.user,payment_id=payment_id)
        order = Order.objects.get(user=request.user, order_number=order_number, is_ordered=True)
        orderproduct = OrderProduct.objects.filter(user=request.user, payment=payment, order=order)



        total = 0
        for orderP in orderproduct:
            total+= orderP.quantity * orderP.product_price

        mail_subject = 'Thank you for your order'
        message = render_to_string('orders/order_recieved_email.html', {
                    'user':request.user,
                    'orderproduct':orderproduct,
                    'order_number':order_number,
                    'payment_id':payment_id,
                    'current_date':current_date,
                    'order':order,
                    'total':total,
                    'for':'user'

                })
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

        mail_subject = 'Got New Order'
        message = render_to_string('orders/order_recieved_email.html', {
                    'user':request.user,
                    'orderproduct':orderproduct,
                    'order_number':order_number,
                    'payment_id':payment_id,
                    'current_date':current_date,
                    'order':order,
                    'total':total,
                    'for':'admin'

                })
        
        take_email = Order.objects.get(order_number = order_number, is_ordered=True)
        state_name = take_email.state.state
        email_add = AddEmailAddress.objects.get(state__state =  state_name)

        to_email = email_add.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

        to_email = 'aacs807@gmail.com'
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

    else:
        cart = Cart.objects.get(cart_id= _cart_item(request))
        cart_item = CartItem.objects.filter(cart =cart, is_active=True)
        a=None
        for carts in cart_item:
            a= carts
        a.delete()

        payment = Payment.objects.get(payment_id=payment_id)
        order = Order.objects.get(order_number=order_number, email=email ,is_ordered=True)
        orderproduct = OrderProduct.objects.filter(payment=payment, order=order)

        total = 0
        for orderP in orderproduct:
            total+= orderP.quantity * orderP.product_price

        mail_subject = 'Thank you for your order'
        message = render_to_string('orders/order_recieved_email.html', {
                    'user':request.user,
                    'orderproduct':orderproduct,
                    'order_number':order_number,
                    'payment_id':payment_id,
                    'current_date':current_date,
                    'order':order,
                    'total':total,
                    'for':'user'

                })
        to_email = email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

        mail_subject = 'Got New Order'
        message = render_to_string('orders/order_recieved_email.html', {
                    'user':request.user,
                    'orderproduct':orderproduct,
                    'order_number':order_number,
                    'payment_id':payment_id,
                    'current_date':current_date,
                    'order':order,
                    'total':total,
                    'for':'admin'

                })
        
        take_email = Order.objects.get(order_number = order_number, is_ordered=True)
        state_name = take_email.state.state
        email_add = AddEmailAddress.objects.get(state__state =  state_name)

        to_email = email_add.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

        to_email = 'aacs807@gmail.com'
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

    context={
        'orderproduct':orderproduct,
        'order_number':order_number,
        'payment_id':payment_id,
        'current_date':current_date,
        'order':order,
        'total':total,
    }
    return render(request, 'orders/order_complete.html', context)






def place_order(request, total=0, quantity=0):
    if request.user.is_authenticated:
        current_user = request.user
        cart_items = CartItem.objects.filter(user=current_user)
    else:
        cart = Cart.objects.get(cart_id= _cart_item(request))
        cart_items = CartItem.objects.filter(cart =cart, is_active=True)
    
    cart_count = cart_items.count()
    if cart_count<=0:
        return redirect('store')
    for cart_item in cart_items:
        total+=(cart_item.product.price*cart_item.quantity)
        quantity+=cart_item.quantity
    tax = (2*total)/100
    grand_total = total +tax

    if request.method == "POST":
        form =OrderForm(request.POST)

        if form.is_valid():
            data =Order()
            if request.user.is_authenticated:
                data.user=current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            state = request.POST['state']
            data.state = AddState.objects.get(state__iexact = state)
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total =grand_total
            data.tax=tax
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()

            #Generate Order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d =datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number =order_number
            data.save()
            if request.user.is_authenticated:
                order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            else:
                order = Order.objects.get(email=form.cleaned_data['email'], is_ordered=False, order_number=order_number)


            
            context = {
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
                'place_order': True
            }
            return render(request,'orders/payment.html', context)
        else:
            return redirect('checkout')
            
def buy_place_order(request, total=0, quantity=0):
    if request.user.is_authenticated:
        current_user = request.user
        cart_item = CartItem.objects.filter(user=current_user)
        cart_items=None
        for carts in cart_item:
            cart_items = carts
    else:
        cart = Cart.objects.get(cart_id= _cart_item(request))
        cart_item = CartItem.objects.filter(cart =cart, is_active=True)
        cart_items = None
        for carts in cart_item:
            cart_items=carts
    
    # cart_count = cart_items.count()
    # if cart_count<=0:
    #     return redirect('store')

    
    total+=(cart_items.product.price)
    quantity=1
    tax = (2*total)/100
    grand_total = total +tax

    if request.method == "POST":
        form =OrderForm(request.POST)

        if form.is_valid():
            data =Order()
            if request.user.is_authenticated:
                data.user=current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            state = request.POST['state']
            data.state = AddState.objects.get(state__iexact = state)
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total =grand_total
            data.tax=tax
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()

            #Generate Order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d =datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number =order_number
            data.save()
            if request.user.is_authenticated:
                order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            else:
                order = Order.objects.get(email=form.cleaned_data['email'], is_ordered=False, order_number=order_number)


            
            context = {
                'order':order,
                'cart_item':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
                'place_order': False,
            }
            return render(request,'orders/payment.html', context)
        else:
            return redirect('checkout')
            





def place_order_existed_address(request, total=0, quantity=0):
    current_user = request.user
    accounts = Account.objects.get(email = current_user.email)

    user_profile_exist = AddAddress.objects.filter(user=accounts, is_active = True).exists()
    if user_profile_exist:
        cart_items = CartItem.objects.filter(user=current_user)
        cart_count = cart_items.count()
        if cart_count<=0:
            return redirect('store')
        for cart_item in cart_items:
            total+=(cart_item.product.price*cart_item.quantity)
            quantity+=cart_item.quantity
        tax = (2*total)/100
        grand_total = total +tax
        user_profile = AddAddress.objects.get(user=accounts, is_active = True)


        data =Order()
        data.user=current_user
        data.first_name = current_user.first_name
        data.last_name = current_user.last_name
        data.phone = user_profile.phone
        data.email = current_user.email
        data.address_line_1 = user_profile.address_line_1
        data.address_line_2 = user_profile.address_line_2
        data.country = user_profile.country
        data.state = user_profile.state
        data.city = user_profile.city
        data.order_total =grand_total
        data.tax=tax
        data.ip=request.META.get('REMOTE_ADDR')
        data.save()
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d =datetime.date(yr,mt,dt)
        current_date = d.strftime("%Y%m%d")
        order_number = current_date + str(data.id)
        data.order_number =order_number
        data.save()
        order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
                
        context = {
            'order':order,
            'cart_items':cart_items,
            'total':total,
            'tax':tax,
            'grand_total':grand_total,
            'place_order':True
                }
        return render(request,'orders/payment.html', context)

    else:
        messages.error(request, 'Need to add Address First')
        return redirect('add_address')

def buy_place_order_existed_address(request, total=0, quantity=0):
    current_user = request.user
    cart_items=None
    if current_user.is_authenticated:
        accounts = Account.objects.get(email = current_user.email)
        user_profile_exist = AddAddress.objects.filter(user=accounts, is_active = True).exists()
        print(user_profile_exist)
        if user_profile_exist:
            user_profile = AddAddress.objects.get(user=accounts, is_active = True)
            cart_item = CartItem.objects.filter(user=current_user)
            for carts in cart_item:
                cart_items = carts
            
            total+=(cart_items.product.price)
            quantity=1
            tax = (2*total)/100
            grand_total = total +tax
            
            data =Order()
            data.user=current_user
            data.first_name = current_user.first_name
            data.last_name = current_user.last_name
            data.phone = user_profile.phone
            data.email = current_user.email
            data.address_line_1 = user_profile.address_line_1
            data.address_line_2 = user_profile.address_line_2
            data.country = user_profile.country
            data.state = user_profile.state
            data.city = user_profile.city
            data.order_total =grand_total
            data.tax=tax
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()
        
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d =datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number =order_number
            data.save()
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
                    
            context = {
                'order':order,
                'cart_item':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
                'place_order':False
                    }
            return render(request,'orders/payment.html', context)
        
        else:
            messages.error(request, 'Need to add Address First')
            return redirect('add_address')
    
    else:
        return redirect('login')




   

        
      
    
# def buy_now(request, total=0, quantity=0):
#     if request.user.is_authenticated:
#         current_user = request.user
#         buynow = BuyNow.objects.filter(user=current_user)
#     else:
#         cart = Cart.objects.get(cart_id= _cart_item(request))       
#         buynow = BuyNow.objects.filter(cart =cart, is_active=True)
        
    
#     buynow_count = buynow.count()
#     if buynow_count<=0:
#         return redirect('store')

#     for cart_item in cart_items:
#         total+=(cart_item.product.price*cart_item.quantity)
#         quantity+=cart_item.quantity
#     tax = (2*total)/100
#     grand_total = total +tax

#     if request.method == "POST":
#         form =OrderForm(request.POST)

#         if form.is_valid():
#             data =Order()
#             if request.user.is_authenticated:
#                 data.user=current_user
#             data.first_name = form.cleaned_data['first_name']
#             data.last_name = form.cleaned_data['last_name']
#             data.phone = form.cleaned_data['phone']
#             data.email = form.cleaned_data['email']
#             data.address_line_1 = form.cleaned_data['address_line_1']
#             data.address_line_2 = form.cleaned_data['address_line_2']
#             data.country = form.cleaned_data['country']
#             data.state = form.cleaned_data['state']
#             data.city = form.cleaned_data['city']
#             data.order_note = form.cleaned_data['order_note']
#             data.order_total =grand_total
#             data.tax=tax
#             data.ip=request.META.get('REMOTE_ADDR')
#             data.save()

#             #Generate Order number
#             yr = int(datetime.date.today().strftime('%Y'))
#             dt = int(datetime.date.today().strftime('%d'))
#             mt = int(datetime.date.today().strftime('%m'))
#             d =datetime.date(yr,mt,dt)
#             current_date = d.strftime("%Y%m%d")
#             order_number = current_date + str(data.id)
#             data.order_number =order_number
#             data.save()
#             if request.user.is_authenticated:
#                 order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
#             else:
#                 order = Order.objects.get(email=form.cleaned_data['email'], is_ordered=False, order_number=order_number)


            
#             context = {
#                 'order':order,
#                 'cart_items':cart_items,
#                 'total':total,
#                 'tax':tax,
#                 'grand_total':grand_total,
#             }
#             return render(request,'orders/payment.html', context)
#         else:
#             return redirect('checkout')