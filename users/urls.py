from django.urls import path

from users import views

urlpatterns = [
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterFormView.as_view(), name='register'),
    path('login/', views.LoginFormView.as_view(), name='login'),
    path('edit/', views.EditUserFormView.as_view(), name='edit-user'),
    path('change-password/', views.UserChangePasswordFormView.as_view(), name='change-password-user'),
    path('<slug:slug>/', views.PersonalCabinetUserDetailView.as_view(), name='user-detail'),
]