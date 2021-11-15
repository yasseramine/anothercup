from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from cupboards.models import Cupboard


def cart_contents(request):

    cart_items = []
    total = 0
    count = 0
    cart = request.session.get('cart', {})
    delivery = 0

    for item_id, item_data in cart.items():

        cupboard = get_object_or_404(Cupboard, pk=item_id)  

        for code, quantity in item_data['cupboards_by_code'].items():
            price = float(code.split('#')[4])
            subtotal = quantity * price
            subtotal = format(subtotal, '.2f')
            total += float(subtotal)
            count += quantity

            height = code.split('#')[0]
            width = code.split('#')[1]
            depth = code.split('#')[2]
            shelves = code.split('#')[3]
            dims = f"{height}mm x {width}mm x {depth}mm with {shelves} shelves."
            postage = float(code.split('#')[5])

            postage_subtotal = postage * quantity

            delivery += postage_subtotal

            spec = {
                "height": int(height),
                "width": int(width),
                "depth": int(depth),
                "shelves": int(shelves),
                "dims": dims,
                "postage": postage
            }
            cart_items.append({
                'item_id': item_id,
                'quantity': quantity,
                'cupboard': cupboard,
                "price": price,
                "spec": spec,
                "subtotal": subtotal,
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
