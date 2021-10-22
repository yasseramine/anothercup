from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from cupboards.models import Cupboard


def cart_contents(request):

    cart_items = []
    total = 0
    count = 0
    cart = request.session.get('cart', {})
    delivery = 25.00

    for item_id, item_data in cart.items():

        cupboard = get_object_or_404(Cupboard, pk=item_id)  

        for code, quantity in item_data['cupboards_by_code'].items():
            price = float(code.split('#')[4])
            total += quantity * price
            count += quantity
            cart_items.append({
                'item_id': item_id,
                'quantity': quantity,
                'cupboard': cupboard,
                'code': code,
            })

    grand_total = delivery + total
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'count': count,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    return context
