from django.contrib.auth import logout, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages

from users.forms import UserCreationForm, LoginForm


class LogoutView(LoginRequiredMixin, generic.View):
    template_name = 'users/logout.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if self.request.user.is_authenticated:
            logout(request)
            return redirect('home')


class RegisterFormView(generic.FormView):
    form_class = UserCreationForm
    template_name = 'users/RegisterFormView.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form: UserCreationForm):
        cleaned_data = form.cleaned_data
        email = form.cleaned_data['email']
        username = email.split('@')[0]

        user_model = get_user_model()
        user = user_model.objects.create_user(email=email, username=username, password=form.cleaned_data['password1'])
        login(self.request, user=user)

        messages.success(self.request, 'Регистрация прошла успешно!')
        return super().form_valid(form)


class LoginFormView(generic.FormView):
    form_class = LoginForm
    template_name = 'users/LoginFormView.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user_login = form.cleaned_data.get('user_login')
        login(self.request, user_login)

        messages.success(self.request, 'Вы успешно вошли на сайт!')
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
