from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from .contexts import cart_contents

from cupboards.models import Cupboard

# Create your views here.


def view_cart(request):
    """A view that renders a page showing the cart contents"""

    return render(request, 'cart/cart.html')


def add_to_cart(request, cupboard_id, code):
    """ Add a quantity of the specified product to the shopping bag """

    # redirect_url = request.POST.get('redirect_url')
    
    cupboard = get_object_or_404(Cupboard, pk=cupboard_id)
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    if cupboard_id in list(cart.keys()):
        if code in cart[cupboard_id]['cupboards_by_code'].keys():
            cart[cupboard_id]['cupboards_by_code'][code] += quantity
            messages.success(request, f'Cart updated')
        else:
            cart[cupboard_id]['cupboards_by_code'][code] = quantity
            messages.success(request, f"{cupboard.name} added to cart")
    else:
        cart[cupboard_id] = {'cupboards_by_code': {code: quantity}}
        messages.success(request, f"{cupboard.name} added to cart")

    request.session['cart'] = cart
    print(cart)
    return redirect('view_cart')
