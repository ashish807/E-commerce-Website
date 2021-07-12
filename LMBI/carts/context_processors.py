from .models import Cart, CartItem
from .views import _cart_item
from store.models import Product
from django.core.exceptions import ObjectDoesNotExist

def counter(request):
    cart_count =0
    if 'admin' in request.path:
        return {}
    
    else:
        try:
            total = 0
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:
                cart = Cart.objects.filter(cart_id=_cart_item(request))
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count+=cart_item.quantity
                total += cart_item.quantity * cart_item.product.price
        except Cart.DoesNotExist:
            cart_count=0
    return dict(cart_count=cart_count, total=total)


def navCart(request):
    tax=0
    grand_total=0
    total=0
    quantity=0
    cart_items=None
    try:
        
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id= _cart_item(request))
            cart_items = CartItem.objects.filter(cart =cart, is_active=True)
        for cart_item in cart_items:
            total+=(cart_item.product.price * cart_item.quantity)
            quantity+=cart_item.quantity
        tax= (2*total)/100
        grand_total = total+tax
    except ObjectDoesNotExist:
        pass

    context = {
        'grand_totalNAV':grand_total,
        'taxNAV':tax,
        'totalNAV': total,
        'quantityNAV': quantity,
        'cart_itemss': cart_items,
    }
    
    return context