from basket.models import Category


def categories(request):
    return {'categories': Category.objects.all()}


def cart_context(request):
    session = request.session
    cart = session.get('cart', {})
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    get_num_of_items = sum(item['quantity'] for item in cart.values())

    return {
        'cart_items': cart,
        'total_price': total_price,
        'get_num_of_items': get_num_of_items,
    }