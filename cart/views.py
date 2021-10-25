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
    
    cupboard = get_object_or_404(Cupboard, pk=cupboard_id)
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    if cupboard_id in list(cart.keys()):
        if code in cart[cupboard_id]['cupboards_by_code'].keys():
            cart[cupboard_id]['cupboards_by_code'][code] += quantity
            messages.success(request, f'Cart quantity updated!')
        else:
            cart[cupboard_id]['cupboards_by_code'][code] = quantity
            messages.success(request, f"{quantity} {cupboard.name} added to cart.")
    else:
        cart[cupboard_id] = {'cupboards_by_code': {code: quantity}}
        messages.success(request, f"{quantity} {cupboard.name} added to cart.")

    request.session['cart'] = cart
    print(cart)
    return redirect('view_cart')


def update_cart(request, item_id):
    """Update the quantity  in the cart of a design with dimensions"""

    cupboard = get_object_or_404(Cupboard, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    code = request.POST['spec_code']
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[item_id]['cupboards_by_code'][code] = quantity
        messages.success(request, 
                            f'Quantity in cart updated to {cart[item_id]["cupboards_by_code"][code]}.')
    else:
        del cart[item_id]['cupboards_by_code'][code]
        if not cart[item_id]['cupboards_by_code']:
            cart.pop(item_id)
        messages.info(request, f'Item removed from cart.')

    request.session['cart'] = cart
    return redirect('view_cart')


def remove_item(request, item_id):
    """Remove an item from the shopping cart"""

    try:
        cupboard = get_object_or_404(Cupboard, pk=item_id)
        code = request.POST['spec_code']
        cart = request.session.get('cart', {})

        del cart[item_id]['cupboards_by_code'][code]
        if not cart[item_id]['cupboards_by_code']:
            cart.pop(item_id)
            messages.info(request, f'Item removed from cart.')

        request.session['cart'] = cart
        return redirect('view_cart')

    except Exception as e:
        messages.error(request, f'Error removing item: {e}.')
        return HttpResponse(status=500)
 


