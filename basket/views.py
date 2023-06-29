from django.views import generic

from .models import Category, MainPart


class CatalogListView(generic.ListView):
    model = Category
    template_name = 'basket/catalog.html'
    context_object_name = 'categories'


class MainPartDetailView(generic.DetailView):
    model = MainPart
    template_name = 'basket/part_detail.html'
    context_object_name = 'mainpart'
