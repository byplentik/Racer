from importlib import import_module

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model as User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from users.models import DeliveryAddressModel
from .forms import CheckoutFromCartForm
from .mixins import CreateSessionKeyMixin
from .models import Category, Part, CheckoutCart, OrderedPart, Motorcycle, SpecifiedDeliveryAddressModel


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

        num_items = sum(item['quantity'] for item in cart.values())
        return JsonResponse({'num_items': num_items, 'part_name': part.name})


class RemoveOnePartFromCartView(CreateSessionKeyMixin, generic.View):

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


class AddOnePartFromCartView(CreateSessionKeyMixin, generic.View):

    def post(self, request, part_id):
        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        session = SessionStore(session_key=request.session.session_key)
        cart = session.get('cart', {})

        # Увеличиваем количество товара в корзине
        if str(part_id) in cart:
            cart[str(part_id)]['quantity'] += 1

        session['cart'] = cart
        session.save()

        # Вычисляем обновленную сумму и количество товаров в корзине
        total_price = sum(item['price'] * item['quantity'] for item in cart.values())
        num_items = sum(item['quantity'] for item in cart.values())

        return JsonResponse(
            {'total_price': total_price, 'num_items': num_items, 'quantity': cart[str(part_id)]['quantity'], 'partId': part_id})


class CartSessionDetailView(CreateSessionKeyMixin, generic.TemplateView):
    template_name = 'basket/cart-user-detail.html'


class CheckoutFromCartView(CreateSessionKeyMixin, generic.FormView):
    template_name = 'basket/checkout-form.html'
    form_class = CheckoutFromCartForm
    success_url = reverse_lazy('thank-you-page')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        if user.is_authenticated:
            addresses = DeliveryAddressModel.objects.filter(user=user)
            if addresses.count() > 0:
                form.fields['name_address'].queryset = addresses
        return form

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form: CheckoutFromCartForm):
        user = self.request.user
        cart = self.request.session.get('cart', {})
        total_price = sum(item['price'] * item['quantity'] for item in cart.values())
        cleaned_data = form.cleaned_data

        if user.is_authenticated:
            # Если существует поле name_address, значит адрес есть
            if cleaned_data.get('name_address', False):
                address_from_db = cleaned_data['name_address']

                # Если данные из формы верны с cleaned_data
                if self._is_address_valid(address_from_db, cleaned_data):
                    address = SpecifiedDeliveryAddressModel.objects.create(
                        full_name=address_from_db.full_name,
                        phone_number=address_from_db.phone_number,
                        postal_code=address_from_db.postal_code,
                        country=address_from_db.country,
                        delivery_address=address_from_db.delivery_address,
                        user=address_from_db.user,
                    )
                    checkout_cart = self._create_checkout_cart(user, total_price, address, cleaned_data)
                else:
                    # Обновляем адрес и сохраняем экземпляр
                    self._update_address(address_from_db, cleaned_data)
                    address = SpecifiedDeliveryAddressModel.objects.create(
                        full_name=address_from_db.full_name,
                        phone_number=address_from_db.phone_number,
                        postal_code=address_from_db.postal_code,
                        country=address_from_db.country,
                        delivery_address=address_from_db.delivery_address,
                        user=address_from_db.user,
                    )
                    checkout_cart = self._create_checkout_cart(user, total_price, address, cleaned_data)

            # Если отсутствует cleaned_data['name_address'], то есть адреса у пользователя нет
            else:
                address = SpecifiedDeliveryAddressModel.objects.create(
                    full_name=cleaned_data['full_name'],
                    phone_number=cleaned_data['phone_number'],
                    postal_code=cleaned_data['postal_code'],
                    country=cleaned_data['country'],
                    delivery_address=cleaned_data['delivery_address'],
                    user=user,
                )

                checkout_cart = self._create_checkout_cart(user, total_price, address, cleaned_data)
                address.save()

        # Если пользователь не авторизован
        else:
            # Создаем пользователя и адрес
            user, address = self._create_user_and_address(cleaned_data)
            checkout_cart = self._create_checkout_cart(user, total_price, address, cleaned_data)

            address.save()

        # Добавляем запчасти в корзину
        self._create_ordered_parts(cart, checkout_cart)
        messages.success(self.request, f'{checkout_cart.pk}')
        return super().form_valid(form)

    def _create_user_and_address(self, cleaned_data):
        email = cleaned_data['email']
        user, created = User().objects.get_or_create(email=email)

        if created:
            user.username = email.split('@')[0]
            user.set_password('1234')
            user.save()

        # Добавляем его адрес в бд
        address = SpecifiedDeliveryAddressModel.objects.create(
            full_name=cleaned_data['full_name'],
            phone_number=cleaned_data['phone_number'],
            postal_code=cleaned_data['postal_code'],
            country=cleaned_data['country'],
            delivery_address=cleaned_data['delivery_address'],
            user=user,
        )
        return user, address

    def _create_ordered_parts(self, cart, checkout_cart):
        for part_id, cart_item in cart.items():
            part = Part.objects.get(pk=part_id)
            quantity = cart_item['quantity']
            OrderedPart.objects.create(cart=checkout_cart, part=part, quantity=quantity)
        self.request.session['cart'] = {}

    def _create_checkout_cart(self, user, total_price, delivery_address, cleaned_data):
        checkout_cart = CheckoutCart.objects.create(
            user=user,
            total_price=total_price,
            delivery_address=delivery_address,
            comment=cleaned_data['comment'],
        )
        return checkout_cart

    def _is_address_valid(self, address_from_db, cleaned_data):
        return (
            address_from_db.full_name == cleaned_data['full_name'] and
            address_from_db.phone_number == cleaned_data['phone_number'] and
            address_from_db.postal_code == cleaned_data['postal_code'] and
            address_from_db.country == cleaned_data['country'] and
            address_from_db.delivery_address == cleaned_data['delivery_address']
        )

    def _update_address(self, address_from_db, cleaned_data):
        address_from_db.full_name = cleaned_data['full_name']
        address_from_db.phone_number = cleaned_data['phone_number']
        address_from_db.postal_code = cleaned_data['postal_code']
        address_from_db.country = cleaned_data['country']
        address_from_db.delivery_address = cleaned_data['delivery_address']
        address_from_db.save()

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        if user.is_authenticated:
            address = DeliveryAddressModel.objects.filter(user=user).first()
            if address is not None:
                initial['full_name'] = address.full_name
                initial['phone_number'] = address.phone_number
                initial['postal_code'] = address.postal_code
                initial['country'] = address.country
                initial['delivery_address'] = address.delivery_address
        return initial


def get_address_details(request):
    address_id = request.GET.get('address_id')
    address = get_object_or_404(DeliveryAddressModel, pk=address_id)

    data = {
        'full_name': address.full_name,
        'phone_number': address.phone_number,
        'postal_code': address.postal_code,
        'country': address.country,
        'delivery_address': address.delivery_address,
    }
    return JsonResponse(data)


class CreatedOrdersUserListView(CreateSessionKeyMixin, generic.ListView):
    model = CheckoutCart
    template_name = 'basket/CreatedOrdersUserListView.html'
    context_object_name = 'orders'

    def get_queryset(self):
        user = self.request.user
        queryset = CheckoutCart.objects.filter(user=user).order_by('-created_at')
        return queryset


class ThankYouPageTemplateView(generic.TemplateView):
    template_name = 'basket/ThankYouPageTemplateView.html'
