from django.urls import path

from users import views
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    # Вход и выход на сайте
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterFormView.as_view(), name='register'),
    path('login/', views.LoginFormView.as_view(), name='login'),

    # Сброс пароля
    path('reset_password/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset_password/done/', PasswordResetDoneView.as_view(template_name='users/password_reset/password_reset_done.html'), name='password_reset_done'),
    path('reset_password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password/complete/', PasswordResetCompleteView.as_view(template_name='users/password_reset/password_reset_complete.html'), name='password_reset_complete'),

    # Личный кабинет
    path('user/edit/', views.EditUserFormView.as_view(), name='edit-user'),
    path('user/change-password/', views.UserChangePasswordFormView.as_view(), name='change-password-user'),
    path('user/addresses/', views.DeliveryAddressUserListView.as_view(), name='addresses-list'),
    path('user/add-address/', views.DeliveryAddressAddFormView.as_view(), name='add-address'),
    path('user/delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('user/<slug:slug>/', views.PersonalCabinetUserDetailView.as_view(), name='user-detail'),
]