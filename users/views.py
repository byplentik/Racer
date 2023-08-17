import re
import secrets


import requests
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from dotenv import load_dotenv

from .forms import PhoneNumberForm, VerificationCodeForm, PersonalСabinetForm
from .models import CustomUser

load_dotenv()


class LoginView(generic.FormView):
    """
    Представление Django для обработки входа пользователя в систему.

    Представление отображает форму для ввода номера телефона и отправляет проверочный код на введенный номер.
    Класс проверяет принадлежность введенного номера к странам СНГ (Россия, Казахстан) и форматирует его в стандартный
    формат (8). Затем он отправляет POST-запрос к SMS API-сервису для отправки проверочного кода на номер телефона.
    В случае успешного выполнения запроса пользователь перенаправляется на страницу с проверочным кодом.
    В противном случае выдается сообщение об ошибке.
    """

    template_name = 'users/login.html'
    form_class = PhoneNumberForm
    success_url = reverse_lazy('verify_code')

    def is_sng_number(self, number: str) -> bool:
        """
        Проверяем, является ли введенный номер из формы к Странам СНГ
        (Россия, Казахстан)
        """
        return re.match(r'^(\+?7|\+?8)', number) is not None

    def to_correct_number(self, number: str) -> str:
        """
        Форматирование телефонного номера в стандартный формат.
        """
        if number.startswith('+7') or number.startswith('+8'):
            return '8' + number[2:]
        if number.startswith('7'):
            return '8' + number[1:]
        return number

    def form_valid(self, form: PhoneNumberForm):
        code = str(secrets.randbelow(1000000)).zfill(6)
        number = form.cleaned_data['phone_number']
        if not self.is_sng_number(number):
            form.add_error('phone_number', 'Укажите корректный номер телефона')
            return self.form_invalid(form)
        correct_number = self.to_correct_number(number)

        # Сохраняем код и номер телефона в сессии пользователя
        self.request.session['auth_code'] = code
        self.request.session['phone_number'] = correct_number

        # Отправка post запроса на API сервис для отправки сообщения
        data = {
            'number': correct_number,
            'text': f'Ваш код верефикации {code}',
            'sign': 'SMS Aero'
        }
        response = requests.post(url=settings.URL_SMS_AERO, auth=(settings.EMAIL, settings.API_KEY), data=data)

        # Проверяем status code
        if response.status_code == 200:
            return super().form_valid(form)
        else:
            form.add_error('phone_number', 'Не удалось отправить SMS')
            return self.form_invalid(form)


class VerifyCodeView(generic.FormView):
    form_class = VerificationCodeForm
    template_name = 'users/verify_code.html'
    success_url = reverse_lazy('cabinet')

    def form_valid(self, form):
        entered_code = form.cleaned_data['code']
        if entered_code == self.request.session.get('auth_code'):
            del self.request.session['auth_code']
            phone_number = self.request.session.get('phone_number')
            try:
                user = CustomUser.objects.get(phone_number=phone_number)
            except Exception:
                user = CustomUser.objects.create(phone_number=phone_number, name='', last_name='')
            finally:
                login(self.request, user)
                del self.request.session['phone_number']
                return super().form_valid(form)
        else:
            form.add_error('code', 'Неверный код')
            return self.form_invalid(form)


class LogoutView(LoginRequiredMixin, generic.View):
    template_name = 'users/logout.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if self.request.user.is_authenticated:
            logout(request)
            return redirect('home')


class PersonalСabinetTemplateView(generic.TemplateView):
    template_name = 'users/personal_cabinet.html'


class PersonalСabinetFormView(generic.FormView):
    template_name = 'users/update-personal-cabinet.html'
    form_class = PersonalСabinetForm
    success_url = reverse_lazy('cabinet')

    def form_valid(self, form):
        user = self.request.user
        user.email = form.cleaned_data['email']
        user.name = form.cleaned_data['name']
        user.last_name = form.cleaned_data['last_name']
        user.delivery_address = form.cleaned_data['delivery_address']
        user.delivery_index = form.cleaned_data['delivery_index']
        user.save()
        return redirect(self.get_success_url())

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial['email'] = user.email
        initial['name'] = user.name
        initial['last_name'] = user.last_name
        initial['delivery_address'] = user.delivery_address
        initial['delivery_index'] = user.delivery_index
        return initial
