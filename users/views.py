from django.contrib.auth import logout, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView


from users.forms import UserCreationForm, \
    LoginForm, EditUserForm, UserChangePasswordForm


class FormViewCustom(generic.FormView):
    def get_success_url(self):
        return reverse_lazy('user-detail', kwargs={'slug': self.request.user.slug})


class LogoutView(LoginRequiredMixin, generic.View):
    template_name = 'users/logout.html'

    def get(self, request):
        return render(request, self.template_name)

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


class PersonalCabinetUserDetailView(generic.DetailView):
    model = get_user_model()
    template_name = 'users/user-detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class EditUserFormView(FormViewCustom):
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


class UserChangePasswordFormView(PasswordChangeView):
    template_name = 'users/UserChangePasswordFormView.html'
    form_class = UserChangePasswordForm

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Вы успешно сменили пароль!')
        return response

    def get_success_url(self):
        return reverse_lazy('user-detail', kwargs={'slug': self.request.user.slug})