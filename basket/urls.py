from django.urls import path

from . import views

urlpatterns = [
    path('cart/add-to-cart/<int:part_id>/<int:quantity>/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('cart/', views.CartSessionDetailView.as_view(), name='cart-session'),
    path('cart/remove/<int:part_id>/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('catalog/', views.CatalogListView.as_view(), name='catalog'),
    path('catalog/<slug:slug>/', views.MotorcycleDetailView.as_view(), name='motorcycle-detail'),
    path('checkout/', views.CheckoutFromCartView.as_view(), name='checkout-form'),
]
