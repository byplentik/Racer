from django.urls import path

from users import views

urlpatterns = [
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterFormView.as_view(), name='register'),
    path('login/', views.LoginFormView.as_view(), name='login')
]