import pytest
from django.urls import reverse


@pytest.fixture
def create_user(db, django_user_model):
    def make_user(**kwargs):
        if 'phone_number' not in kwargs:
            kwargs['phone_number'] = '7008003030'
        return django_user_model.objects.create(**kwargs)
    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.force_login(user)
        return client, user


@pytest.mark.django_db
def test_home_template_view(client):
    expected_path = '/'
    expected_text = "Это главная страница"

    url = reverse('home')
    response = client.get(url)

    assert url == expected_path
    assert response.status_code == 200
    assert expected_text in response.content.decode()


@pytest.mark.django_db
def test_personal_cabinet_auth_user(auto_login_user):
    client, user = auto_login_user()
    url = reverse('cabinet')

    response = client.get(url)
    assert response.status_code == 200
    assert '7008003030' in response.content.decode()

