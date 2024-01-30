from django.urls import path

from users import views

urlpatterns = [
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterFormView.as_view(), name='register'),
    path('login/', views.LoginFormView.as_view(), name='login'),
    path('user/edit/', views.EditUserFormView.as_view(), name='edit-user'),
    path('user/change-password/', views.UserChangePasswordFormView.as_view(), name='change-password-user'),
    path('user/addresses/', views.DeliveryAddressUserListView.as_view(), name='addresses-list'),
    path('user/add-address/', views.DeliveryAddressAddFormView.as_view(), name='add-address'),
    path('user/delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('user/<slug:slug>/', views.PersonalCabinetUserDetailView.as_view(), name='user-detail'),
]