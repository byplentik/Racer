from importlib import import_module

from django.conf import settings
from django.shortcuts import redirect, render
from django.views import generic
from django.http import JsonResponse

from .models import Category, MainPart, Part
from .mixins import CreateSessionKeyMixin


class HomeView(CreateSessionKeyMixin, generic.View):
    def get(self, request):
        return render(request, 'home.html')


class CatalogListView(CreateSessionKeyMixin, generic.ListView):
    model = Category
    template_name = 'basket/catalog.html'
    context_object_name = 'categories'


class MainPartDetailView(CreateSessionKeyMixin, generic.DetailView):
    model = MainPart
    template_name = 'basket/part_detail.html'
    context_object_name = 'mainpart'


class AddToCartView(CreateSessionKeyMixin, generic.View):
    def post(self, request, part_id, quantity):
        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        session = SessionStore(session_key=request.session.session_key)
        cart = session.get('cart', {})
        cart_item = cart.get(str(part_id), {})

        # Получаем данные запчасти
        part = Part.objects.get(pk=part_id)

        # Добавляем данные запчасти в объект cart_item
        cart_item['quantity'] = cart_item.get('quantity', 0) + quantity
        cart_item['name'] = part.name
        cart_item['price'] = part.price
        cart[str(part_id)] = cart_item
        session['cart'] = cart
        session.save()
        return redirect('catalog')


class RemoveFromCartView(CreateSessionKeyMixin, generic.View):

    def post(self, request, part_id):
        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        session = SessionStore(session_key=request.session.session_key)
        cart = session.get('cart', {})

        # Уменьшаем количество товара в корзине
        if str(part_id) in cart:
            cart[str(part_id)]['quantity'] -= 1

            # Если количество стало меньше или равно 0, удаляем товар из корзины
            if cart[str(part_id)]['quantity'] <= 0:
                del cart[str(part_id)]
                quantity = 0
            else:
                quantity = cart[str(part_id)]['quantity']

            session['cart'] = cart
            session.save()

        # Вычисляем обновленную сумму и количество товаров в корзине
        total_price = sum(item['price'] * item['quantity'] for item in cart.values())
        num_items = sum(item['quantity'] for item in cart.values())

        return JsonResponse({'total_price': total_price, 'num_items': num_items, 'quantity': quantity})


class CartSessionDetailView(CreateSessionKeyMixin, generic.TemplateView):
    template_name = 'basket/cart-session-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session = self.request.session
        cart = session.get('cart', {})
        total_price = sum(item['price'] * item['quantity'] for item in cart.values())
        get_num_of_items = sum(item['quantity'] for item in cart.values())
        context['cart_items'] = cart
        context['total_price'] = total_price
        context['get_num_of_items'] = get_num_of_items
        return context


class CheckoutFromCartView(generic.View):
    pass

