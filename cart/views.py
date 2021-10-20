from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from cupboards.models import Cupboard

# Create your views here.


def view_cart(request):
    """A view that renders a page showing the cart contents"""

    return render(request, 'cart/cart.html')


def add_to_cart(request, cupboard_id, H, W, L, S, dims_code, cost):
    """ Add a quantity of the specified product to the shopping bag """

    cupboard = get_object_or_404(Cupboard, pk=cupboard_id)
    quantity = int(request.POST.get('quantity'))

    cart = request.session.get('cart', {})

    if cupboard_id in list(cart.keys()):
        if dims_code in cart[cupboard_id]['items_by_size'].keys():
            cart[cupboard_id]['items_by_size'][dims_code] += quantity
            messages.success(request, "Cart Updated!")

        else:
            cart[cupboard_id]['items_by_size'][dims_code] = quantity
            messages.success(request, f"{cupboard.name}) added to cart")

    request.session['cart'] = cart
    return redirect('view_cart')