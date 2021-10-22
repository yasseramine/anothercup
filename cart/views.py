from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from .contexts import cart_contents

from cupboards.models import Cupboard

# Create your views here.


def view_cart(request):
    """A view that renders a page showing the cart contents"""

    return render(request, 'cart/cart.html')


def add_to_cart(request, cupboard_id, H, W, D, S, code, cost):
    """ Add a quantity of the specified product to the shopping bag """

    cupboard = get_object_or_404(Cupboard, pk=cupboard_id)
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    new_cupboard_dict = {
                        "code": code,
                        "spec": {
                                'cupboard_id': cupboard_id,
                                'height': H,
                                'width': W,
                                'depth': D,
                                'shelves': S,
                                'cost': cost,
                                'quantity': quantity
                                }
                        }

    if code in list(cart.keys()):
        cart[code][{"quantity": quantity}] += quantity
        messages.success(request, f'Cart updated')

    else:
        cart['code']["quantity"] = quantity
        cart[cart_items].append(new_cupboard_dict)
        messages.success(request, f"{cupboard.name} added to cart")

    print(cart)
    print('new')
    print(new_cupboard_dict)

    request.session['cart'] = cart

    return redirect('view_cart')
