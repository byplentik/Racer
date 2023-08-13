import os
import random
from importlib import import_module

import requests
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model as User, login
from django.core.exceptions import ObjectDoesNotExist


from .models import Category, MainPart, Part, CheckoutCart, OrderedPart
from .mixins import CreateSessionKeyMixin
from .forms import CheckoutFromCartForm, CheckoutFromCartFormNotAuth, VerifyCodeFormAndCreateOrder
from users.views import LoginView

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


class CheckoutFromCartView(LoginRequiredMixin, CreateSessionKeyMixin, generic.FormView):
    template_name = 'basket/checkout-form.html'
    form_class = CheckoutFromCartForm
    success_url = reverse_lazy('cabinet')

    def form_valid(self, form):
        user = self.request.user
        cart = self.request.session.get('cart', {})
        total_price = sum(item['price'] * item['quantity'] for item in cart.values())
        checkout_cart = CheckoutCart.objects.create(user=user, total_price=total_price)

        for part_id, cart_item in cart.items():
            part = Part.objects.get(pk=part_id)
            quantity = cart_item['quantity']
            OrderedPart.objects.create(cart=checkout_cart, part=part, quantity=quantity)
        self.request.session['cart'] = {}
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial['email'] = user.email
        initial['name'] = user.name
        initial['last_name'] = user.last_name
        initial['delivery_address'] = user.delivery_address
        initial['delivery_index'] = user.delivery_index
        return initial


class CheckoutFromCartViewNotAuthenticated(CreateSessionKeyMixin, generic.FormView):
    template_name = 'basket/checkout-form-not-auth.html'
    form_class = CheckoutFromCartFormNotAuth

    def is_sng_number(self, number):
        return number.startswith('7') or number.startswith('8') or number.startswith('+7') or number.startswith('+8')

    def to_correct_number(self, number: str):
        if number.startswith('+7') or number.startswith('+8'):
            return '8' + number[2:]
        if number.startswith('7'):
            return '8' + number[1:]
        return number

    def send_verification_code(self, phone_number):
        if not self.is_sng_number(phone_number):
            return {'error': 'Укажите корректный номер телефона'}

        correct_number = self.to_correct_number(phone_number)
        API_KEY = os.getenv('API_KEY')
        EMAIL = os.getenv('EMAIL')
        code = ''.join(random.choices('123456', k=6))
        url = f'https://{EMAIL}:{API_KEY}@gate.smsaero.ru/v2/sms/send?number={correct_number}&text=Код верефикации: {code}&sign=SMS Aero'
        response = requests.get(url)
        return {'response': response, 'number': correct_number, 'code': code}

    def form_valid(self, form):
        # Код для отправки подтверждения кода
        number = form.cleaned_data['phone_number']
        verification_result = self.send_verification_code(number)

        if 'error' in verification_result:
            form.add_error('phone_number', verification_result['error'])
            return self.form_invalid(form)

        response = verification_result['response']

        if response.status_code == 200:
            # Сохраняем код подтверждения и номер в сессию
            self.request.session['auth_code'] = verification_result['code']
            self.request.session['phone_number'] = verification_result['number']

            # Сохраняем данные пользователя в сессии
            self.request.session['form_data'] = {
                'email': form.cleaned_data['email'],
                'name': form.cleaned_data['name'],
                'last_name': form.cleaned_data['last_name'],
                'delivery_address': form.cleaned_data['delivery_address'],
                'delivery_index': form.cleaned_data['delivery_index'],
            }
            return redirect('verified-checkout')
        else:
            form.add_error('phone_number', 'Не удалось отправить код верификации, повторите попытку')
            return self.form_invalid(form)


class VerifyCodeViewAndCreateOrder(generic.FormView):
    form_class = VerifyCodeFormAndCreateOrder
    template_name = 'basket/verify_code_for_not_auth.html'

    def form_valid(self, form):
        entered_code = form.cleaned_data['code']
        if entered_code == self.request.session.get('auth_code'):
            del self.request.session['auth_code']
            phone_number = self.request.session.get('phone_number')
            form_data = self.request.session.get('form_data')
            try:
                user = User().objects.get(phone_number=phone_number)
            except Exception:
                user = User().objects.create(phone_number=phone_number, **form_data)
            finally:
                # Код для оформления корзины
                cart = self.request.session.get('cart', {})
                total_price = sum(item['price'] * item['quantity'] for item in cart.values())
                checkout_cart = CheckoutCart.objects.create(user=user, total_price=total_price)
                for part_id, cart_item in cart.items():
                    part = Part.objects.get(pk=part_id)
                    quantity = cart_item['quantity']
                    OrderedPart.objects.create(cart=checkout_cart, part=part, quantity=quantity)

                self.request.session['cart'] = {}
                login(self.request, user)
                del self.request.session['phone_number']
                return redirect('cabinet')
        else:
            form.add_error('code', 'Неверный код')
            return self.form_invalid(form)