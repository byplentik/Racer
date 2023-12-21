import pytest
from django.urls import reverse

from basket.models import Category, Motorcycle


@pytest.mark.django_db
def test_catalog_list_view(client):
    category1 = Category.objects.create(name='category 1')
    category2 = Category.objects.create(name='category 2')

    moto1 = Motorcycle.objects.create(name='moto1', category=category1, slug='moto1')
    moto2 = Motorcycle.objects.create(name='moto2', category=category2, slug='moto2')

    url = reverse('catalog')
    response = client.get(url)

    assert response.status_code == 200
    assert url == '/basket/catalog/'
    assert 'category 1' == str(Category.objects.get(pk=1))
    assert len(Category.objects.all()) == 2
    assert len(Motorcycle.objects.all()) == 2
    assert 'moto1' and 'moto2' in response.content.decode()
    assert moto1.category != moto2.category

