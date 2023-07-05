from .models import Cart


def display_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        return {'cart': cart}
    return {'cart': 'Not authenticated'}