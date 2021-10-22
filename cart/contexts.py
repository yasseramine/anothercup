from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from cupboards.models import Cupboard


def cart_contents(request):

    cart_items = []
    total = 0
    count = 0
    cart = request.session.get('cart', {"cart_items": cart_items, "total": total, "count": count})
    delivery = 25.00

    # print(cart)

    # cupboard = get_object_or_404(Cupboard,
    #                             pk=cart["cupboard_id"])

    # cart_items = WHAT

    # print(cupboard)

    # cart = {
    #     'cart_items': cart_items,
    #     'total': total,
    #     'count': count,
    #     'delivery': delivery,
    #     # 'grand_total': grand_total
    # }

    return cart