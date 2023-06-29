from django.urls import path

from . import views

urlpatterns = [
    path('catalog/', views.CatalogListView.as_view(), name='catalog'),
    path('catalog/<slug:slug>/', views.MainPartDetailView.as_view(), name='part-detail')
]
