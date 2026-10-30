import os

import pytest
from django.contrib.auth.models import User
from django.core.cache import cache

from properties.models import Category, Property

os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'

PASSWORD = 'StrongPass123!'


@pytest.fixture(autouse=True)
def fast_passwords(settings):
    settings.PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
    cache.clear()


@pytest.fixture
def owner(transactional_db):
    return User.objects.create_user('owner', password=PASSWORD)


@pytest.fixture
def stranger(transactional_db):
    return User.objects.create_user('stranger', password=PASSWORD)


@pytest.fixture
def category(transactional_db):
    return Category.objects.create(name='Квартира', slug='kvartira')


@pytest.fixture
def flat(owner, category):
    return Property.objects.create(
        title='Квартира на Печерську', price=150000, deal_type='sale', area_sqm=60, rooms=2,
        address='Київ, Печерськ', latitude=50.44, longitude=30.54, owner=owner, category=category,
    )


@pytest.fixture
def login(page, live_server):
    def do_login(username, password=PASSWORD):
        page.goto(f'{live_server.url}/login/')
        page.fill('input[name="username"]', username)
        page.fill('input[name="password"]', password)
        page.click('form.plain-form button[type="submit"]')
    return do_login
