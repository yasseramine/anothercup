from django.shortcuts import render

# Create your views here.


def view_cart(request):
    """A view that renders a page showing the cart contents"""


    return render(request, 'cart/cart.html')


def add_to_cart(request, cupboard_id):
    """ Add a quantity of the specified product to the shopping bag """

