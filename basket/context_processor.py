from .models import Cart


def display_cart(request):
    if request.user.is_authenticated:
        try:
            Cart.objects.filter(user=request.user).exists()
            cart = Cart.objects.get(user=request.user)
            return {'cart': cart}
        except Exception as ex:
            cart = Cart.objects.get_or_create(user=request.user, completed=False)
            return {'cart': cart}
    return {'cart': 'Not authenticated'}