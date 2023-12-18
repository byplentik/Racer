from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import generic


class LogoutView(LoginRequiredMixin, generic.View):
    template_name = 'users/logout.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if self.request.user.is_authenticated:
            logout(request)
            return redirect('home')
