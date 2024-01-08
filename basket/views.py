from importlib import import_module

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

# from .forms import CheckoutFromCartForm
from .mixins import CreateSessionKeyMixin
from .models import Category, Part, CheckoutCart, OrderedPart, Motorcycle


class CatalogListView(CreateSessionKeyMixin, generic.ListView):
    model = Category
    template_name = 'basket/catalog.html'
    context_object_name = 'categories'


class MotorcycleDetailView(CreateSessionKeyMixin, generic.DetailView):
    model = Motorcycle
    template_name = 'basket/part_detail.html'
    context_object_name = 'motorcycle'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        motorcycle = self.get_object()

        # Фильтруем MainPart, чтобы получить только те, у которых есть связанные Part.price > 0
        main_parts_with_price = motorcycle.mainpart_set.filter(part__price__gt=0).distinct()

        context['main_parts'] = main_parts_with_price
        return context


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

        return JsonResponse(
            {'total_price': total_price, 'num_items': num_items, 'quantity': quantity, 'partId': part_id})


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

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.template_name = 'basket/cart-user-detail.html'
        return super().get(request, *args, **kwargs)


# class CheckoutFromCartView(LoginRequiredMixin, CreateSessionKeyMixin, generic.FormView):
#     template_name = 'basket/checkout-form.html'
#     form_class = CheckoutFromCartForm
#     success_url = reverse_lazy('home')

    # def form_valid(self, form):
    #     user = self.request.user
    #     cart = self.request.session.get('cart', {})
    #     total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    #     checkout_cart = CheckoutCart.objects.create(user=user, total_price=total_price)
    #
    #     for part_id, cart_item in cart.items():
    #         part = Part.objects.get(pk=part_id)
    #         quantity = cart_item['quantity']
    #         OrderedPart.objects.create(cart=checkout_cart, part=part, quantity=quantity)
    #     self.request.session['cart'] = {}
    #     return super().form_valid(form)
    #
    # def get_initial(self):
    #     initial = super().get_initial()
    #     user = self.request.user
    #     initial['email'] = user.email
    #     initial['name'] = user.name
    #     initial['last_name'] = user.last_name
    #     initial['delivery_address'] = user.delivery_address
    #     initial['delivery_index'] = user.delivery_index
    #     return initial

