from django.urls import path

from users import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('verify-code/', views.VerifyCodeView.as_view(), name='verify_code'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('cabinet/update/', views.PersonalСabinetFormView.as_view(), name='cabinet_update'),
    path('cabinet/', views.PersonalСabinetTemplateView.as_view(), name='cabinet'),
]