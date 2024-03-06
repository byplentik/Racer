from importlib import import_module

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model as User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django_mail_admin import mail
from django_mail_admin.models import EmailTemplate, TemplateVariable
from django_mail_admin.utils import PRIORITY

from users.models import DeliveryAddressModel
from .forms import CheckoutFromCartForm, PartSearchForm
from .mixins import CreateSessionKeyMixin
from .models import Category, Part, CheckoutCart, OrderedPart, Motorcycle, SpecifiedDeliveryAddressModel

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


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
        main_parts_with_price = motorcycle.mainpart_set.all()

        if motorcycle.engines.exists():
            context['url_engines'] = motorcycle.engines.all()

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
            user, address, created = self._create_user_and_address(cleaned_data)
            checkout_cart = self._create_checkout_cart(user, total_price, address, cleaned_data)
            address.save()

        # Добавляем запчасти в корзину
        self._create_ordered_parts(cart, checkout_cart)
        self.send_email_created_user(user, checkout_cart, created)

        messages.success(self.request, f'{checkout_cart.pk}')
        return super().form_valid(form)

    def send_email_created_user(self, user, checkout_cart, created):
        template = EmailTemplate.objects.get(name="Шаблон при оформлении заказа")

        # Рендер html
        html_list_parts = '<table border="1">\n'
        html_list_parts += '<tr><th>Наименование</th><th>Цена</th><th>Кол-во</th></tr>\n'
        for ordered_part in checkout_cart.ordered_parts.all():
            html_list_parts += f'<tr><td>{ordered_part.part.name}</td><td>{ordered_part.part.price} р.</td><td>{ordered_part.quantity}</td></tr>\n'
        html_list_parts += '</table>'

        variable_dict = {
            'created': created,
            'number_cart': checkout_cart.pk,
            'subject': f'Вы создали заказ №{checkout_cart.pk} на сайте racer-parts.ru',
            'ordered_parts': html_list_parts,
            'total_price': checkout_cart.total_price,
        }

        # Генерация ссылки для сброса пароля если пользователь создан
        if created:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            reset_url = self.request.build_absolute_uri(reset_url)

            html_reset_url = '<p>Так как вы впервые оформили заказ на нашем сайте, вы можете сбросить пароль по следующей ссылке и войти в личный кабинет:</p>\n'
            html_reset_url += f'<p style="color: red;"><strrong>Ваше имя пользователя (на случай, если вы его забыли):</strong> { user.email }<p>\n'
            html_reset_url += f'{reset_url}\n<hr>'

            variable_dict['html_reset_url'] = html_reset_url

        mail.send('ilyasablin000@yandex.ru',
                  user.email,
                  template=template,
                  priority=PRIORITY.now,
                  variable_dict=variable_dict
                  )

    def _create_user_and_address(self, cleaned_data):
        email = cleaned_data['email']
        user, created = User().objects.get_or_create(email=email)

        if created:
            user.username = email.split('@')[0]
            user.set_password(User().objects.make_random_password())
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
        return user, address, created

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


class PartSearchListView(generic.ListView):
    template_name = 'basket/PartSearchListView.html'
    model = Part
    context_object_name = 'parts'
    form_class = PartSearchForm

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            search_text = form.cleaned_data['text']
            return Part.objects.filter(name__icontains=search_text)
        return Part.objects.all()