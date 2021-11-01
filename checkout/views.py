from django.shortcuts import render, redirect, reverse
from django.contrib import messages

# Create your views here.
from .forms import OrderForm


def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is currently empty.")
        return redirect(reverse('cupboards'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51JY91EGe4ow3O78WoZ8vB4oxMAI2WfjAtzS9xbCXXXhMxPxAgea3xYDwMQabMtsFtMHdbFAqLieOd7SX20N9L7N700CHUczCPa',
        'client_secret': 'test client secret'
    }

    return render(request, template, context)