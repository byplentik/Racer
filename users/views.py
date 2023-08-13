import os
import random

import requests
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from dotenv import load_dotenv

from .forms import PhoneNumberForm, VerificationCodeForm, PersonalСabinetForm
from .models import CustomUser

load_dotenv()


class LoginView(generic.View):
    template_name = 'users/login.html'

    def is_sng_number(self, number):
        return number.startswith('7') or number.startswith('8') or number.startswith('+7') or number.startswith('+8')

    def to_correct_number(self, number: str):
        if number.startswith('+7') or number.startswith('+8'):
            return '8' + number[2:]
        if number.startswith('7'):
            return '8' + number[1:]
        return number

    def get(self, request):
        form_class = PhoneNumberForm()
        return render(request, 'users/login.html', {'form': form_class})

    def post(self, request):
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            API_KEY = os.getenv('API_KEY')
            EMAIL = os.getenv('EMAIL')
            code = ''.join(random.choices('123456', k=6))
            number = form.cleaned_data['phone_number']
            if not self.is_sng_number(number):
                form.add_error('phone_number', 'Укажите корректный номер телефона')
                return render(request, self.template_name, {'form': form})
            correct_number = self.to_correct_number(number)
            request.session['auth_code'] = code
            request.session['phone_number'] = correct_number
            url = f'https://{EMAIL}:{API_KEY}@gate.smsaero.ru/v2/sms/send?number={number}&text=Код верефикации: {code}&sign=SMS Aero'
            response = requests.get(url)
            if response.status_code == 200:
                return redirect('verify_code')
            else:
                return render(request, self.template_name, {'form': form, 'error_message': 'Не удалось отправить SMS'})
        return render(request, self.template_name, {'form': form})


class VerifyCodeView(generic.View):
    form_class = VerificationCodeForm
    template_name = 'users/verify_code.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['code']
            if entered_code == request.session.get('auth_code'):
                del request.session['auth_code']
                phone_number = request.session.get('phone_number')
                try:
                    user = CustomUser.objects.get(phone_number=phone_number)
                except Exception:
                    user = CustomUser.objects.create(phone_number=phone_number, name='', last_name='')
                finally:
                    login(request, user)
                    del request.session['phone_number']
                    return redirect('cabinet')
            else:
                form.add_error('code', 'Неверный код')

        return render(request, self.template_name, {'form': form})


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
