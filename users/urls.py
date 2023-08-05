from django.urls import path

from .views import LoginView, VerifyCodeView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify_code'),
    path('logout/', LogoutView.as_view(), name='logout'),
]