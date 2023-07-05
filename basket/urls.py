from django.urls import path

from . import views

urlpatterns = [
    path('cart/session/', views.CartSessionDetailView.as_view(), name='cart-session'),
    path('catalog/', views.CatalogListView.as_view(), name='catalog'),
    path('catalog/<slug:slug>/', views.MainPartDetailView.as_view(), name='part-detail'),
    path('cart/<pk>/', views.CartDetailView.as_view(), name='cart-detail'),
    path('add-to-cart/<int:part_id>/<int:quantity>/', views.AddToCartView.as_view(), name='add-to-cart'),
]
