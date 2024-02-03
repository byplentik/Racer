from django.urls import path

from . import views

urlpatterns = [
    path('cart/add-to-cart/<int:part_id>/<int:quantity>/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('cart/remove/<int:part_id>/', views.RemoveOnePartFromCartView.as_view(), name='remove-from-cart'),
    path('cart/add-one-part/<int:part_id>/', views.AddOnePartFromCartView.as_view(), name="add-one-part"),
    path('cart/', views.CartSessionDetailView.as_view(), name='cart-session'),
    path('catalog/<slug:slug>/', views.MotorcycleDetailView.as_view(), name='motorcycle-detail'),
    path('catalog/', views.CatalogListView.as_view(), name='catalog'),
    path('checkout/', views.CheckoutFromCartView.as_view(), name='checkout-form'),
    path('user/orders/', views.CreatedOrdersUserListView.as_view(), name='order-list'),
    path('get_address_details/', views.get_address_details, name='get_address_details'),
    path('thankyou_page/', views.ThankYouPageTemplateView.as_view(), name='thank-you-page'),
    path('search/', views.PartSearchListView.as_view(), name='part_search_list'),
]
