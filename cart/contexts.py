from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from cupboards.models import Cupboard


def cart_contents(request):

    cart_items = []
    total = 0
    product_count = 0
    cart = request.session.get('cart', {})

    context = {
        
    }

    return context 