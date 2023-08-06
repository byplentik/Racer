from importlib import import_module

from django.conf import settings
from django.shortcuts import redirect, render
from django.views import generic

from .models import Category, MainPart, Part


class HomeView(generic.View):
    def get(self, request):
        if request.session.session_key is None and request.user.is_authenticated != True:
            request.session['user'] = 'Anonymus user'
        return render(request, 'home.html')


class CatalogListView(generic.ListView):
    model = Category
    template_name = 'basket/catalog.html'
    context_object_name = 'categories'


class MainPartDetailView(generic.DetailView):
    model = MainPart
    template_name = 'basket/part_detail.html'
    context_object_name = 'mainpart'


class AddToCartView(generic.View):
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


class CartSessionDetailView(generic.TemplateView):
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
