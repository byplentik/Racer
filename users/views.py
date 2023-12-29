from django.contrib.auth import logout, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.views.decorators.http import require_POST

from users.models import DeliveryAddressModel
from users.forms import UserCreationForm, DeliveryAddressAddForm, \
    LoginForm, EditUserForm, UserChangePasswordForm


class FormViewCustom(generic.FormView):
    def get_success_url(self):
        return reverse_lazy('user-detail', kwargs={'slug': self.request.user.slug})


class LogoutView(LoginRequiredMixin, generic.View):
    def post(self, request):
        if self.request.user.is_authenticated:
            logout(request)
            return redirect('home')


class RegisterFormView(FormViewCustom):
    form_class = UserCreationForm
    template_name = 'users/RegisterFormView.html'

    def form_valid(self, form: UserCreationForm):
        cleaned_data = form.cleaned_data
        email = cleaned_data['email']
        username = email.split('@')[0]

        user_model = get_user_model()
        user = user_model.objects.create_user(email=email, username=username, password=cleaned_data['password1'])
        login(self.request, user=user)

        messages.success(self.request, 'Регистрация прошла успешно!')
        return super().form_valid(form)


class LoginFormView(FormViewCustom):
    form_class = LoginForm
    template_name = 'users/LoginFormView.html'

    def form_valid(self, form):
        user_login = form.cleaned_data.get('user_login')
        login(self.request, user_login)

        messages.success(self.request, 'Вы успешно вошли на сайт!')
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class PersonalCabinetUserDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    template_name = 'users/user-detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class EditUserFormView(LoginRequiredMixin, FormViewCustom):
    form_class = EditUserForm
    template_name = 'users/EditUserFormView.html'

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial['email'] = user.email
        initial['username'] = user.username
        return initial

    def form_valid(self, form: EditUserForm):
        cleaned_data = form.cleaned_data
        user = self.request.user

        if not user.check_password(cleaned_data['password']):
            form.add_error('password', 'Неверный пароль')
            return self.form_invalid(form)

        user.email = cleaned_data['email']
        user.username = cleaned_data['username']
        user.save()

        messages.success(self.request, 'Вы успешно изменили данные!')
        return super().form_valid(form)


class UserChangePasswordFormView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/UserChangePasswordFormView.html'
    form_class = UserChangePasswordForm

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Вы успешно сменили пароль!')
        return response

    def get_success_url(self):
        return reverse_lazy('user-detail', kwargs={'slug': self.request.user.slug})


class DeliveryAddressUserListView(LoginRequiredMixin, generic.ListView):
    model = DeliveryAddressModel
    template_name = 'users/DeliveryAddressUserListView.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        user = self.request.user
        queryset = DeliveryAddressModel.objects.filter(user=user)
        return queryset


class DeliveryAddressAddFormView(LoginRequiredMixin, generic.FormView):
    form_class = DeliveryAddressAddForm
    template_name = 'users/DeliveryAddressAddFormView.html'
    success_url = reverse_lazy('addresses-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form: DeliveryAddressAddForm):
        form.save()
        messages.success(self.request, 'Вы успешно добавили новый адрес!')
        return super().form_valid(form)


@require_POST
def delete_address(request, address_id):
    address = get_object_or_404(DeliveryAddressModel, id=address_id)
    address.delete()
    return JsonResponse({'success': True})