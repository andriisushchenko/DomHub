import json

from django.contrib.auth.models import User
from django.core.cache import cache
from django.test import TestCase, override_settings

from .models import Category, Property

PASSWORD = 'StrongPass123!'


@override_settings(PASSWORD_HASHERS=['django.contrib.auth.hashers.MD5PasswordHasher'])
class BaseTestCase(TestCase):
    def setUp(self):
        cache.clear()
        self.owner = User.objects.create_user('owner', password=PASSWORD)
        self.stranger = User.objects.create_user('stranger', password=PASSWORD)
        self.admin = User.objects.create_user('admin', password=PASSWORD, is_staff=True)
        self.category = Category.objects.create(name='Квартира', slug='kvartira')
        self.property = Property.objects.create(
            title='Квартира власника', price=100000, deal_type='sale', area_sqm=50, rooms=2,
            address='Київ', owner=self.owner, category=self.category,
        )

    def login(self, username):
        self.client.login(username=username, password=PASSWORD)


class AuthenticationTests(BaseTestCase):
    def test_register_creates_user(self):
        response = self.client.post('/register/', {
            'username': 'newuser', 'password1': PASSWORD, 'password2': PASSWORD,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_with_different_passwords_fails(self):
        self.client.post('/register/', {
            'username': 'newuser', 'password1': PASSWORD, 'password2': 'OtherPass456!',
        })
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_register_with_existing_username_fails(self):
        self.client.post('/register/', {
            'username': 'owner', 'password1': PASSWORD, 'password2': PASSWORD,
        })
        self.assertEqual(User.objects.filter(username='owner').count(), 1)

    def test_login_with_correct_password(self):
        response = self.client.post('/login/', {'username': 'owner', 'password': PASSWORD})
        self.assertEqual(response.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)

    def test_login_with_wrong_password(self):
        response = self.client.post('/login/', {'username': 'owner', 'password': 'wrong'})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_logout(self):
        self.login('owner')
        self.client.post('/logout/')
        self.assertNotIn('_auth_user_id', self.client.session)


class SitePermissionTests(BaseTestCase):
    def test_anonymous_cannot_open_create_page(self):
        response = self.client.get('/property/create/')
        self.assertRedirects(response, '/login/?next=/property/create/')

    def test_logged_in_user_can_open_create_page(self):
        self.login('stranger')
        self.assertEqual(self.client.get('/property/create/').status_code, 200)

    def test_owner_can_open_edit_page(self):
        self.login('owner')
        self.assertEqual(self.client.get(f'/property/{self.property.pk}/edit/').status_code, 200)

    def test_stranger_cannot_open_edit_page(self):
        self.login('stranger')
        self.assertEqual(self.client.get(f'/property/{self.property.pk}/edit/').status_code, 403)

    def test_owner_can_delete(self):
        self.login('owner')
        self.client.post(f'/property/{self.property.pk}/delete/')
        self.assertFalse(Property.objects.filter(pk=self.property.pk).exists())

    def test_stranger_cannot_delete(self):
        self.login('stranger')
        response = self.client.post(f'/property/{self.property.pk}/delete/')
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Property.objects.filter(pk=self.property.pk).exists())


class ApiPermissionTests(BaseTestCase):
    new_property = {
        'title': 'API квартира', 'price': '90000', 'deal_type': 'sale',
        'area_sqm': 40, 'rooms': 1, 'address': 'Одеса',
    }

    def post_json(self, url, data):
        return self.client.post(url, json.dumps(data), content_type='application/json')

    def patch_json(self, url, data):
        return self.client.patch(url, json.dumps(data), content_type='application/json')

    def test_anonymous_can_read(self):
        self.assertEqual(self.client.get('/api/properties/').status_code, 200)

    def test_anonymous_cannot_create(self):
        response = self.post_json('/api/properties/', {**self.new_property, 'category': self.category.pk})
        self.assertEqual(response.status_code, 403)

    def test_logged_in_user_creates_property_as_owner(self):
        self.login('stranger')
        response = self.post_json('/api/properties/', {**self.new_property, 'category': self.category.pk})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['owner'], 'stranger')

    def test_owner_can_update(self):
        self.login('owner')
        response = self.patch_json(f'/api/properties/{self.property.pk}/', {'price': '1000'})
        self.assertEqual(response.status_code, 200)

    def test_stranger_cannot_update(self):
        self.login('stranger')
        response = self.patch_json(f'/api/properties/{self.property.pk}/', {'price': '1'})
        self.assertEqual(response.status_code, 403)

    def test_stranger_cannot_delete(self):
        self.login('stranger')
        response = self.client.delete(f'/api/properties/{self.property.pk}/')
        self.assertEqual(response.status_code, 403)

    def test_regular_user_cannot_create_category(self):
        self.login('stranger')
        response = self.post_json('/api/categories/', {'name': 'Гараж', 'slug': 'garage'})
        self.assertEqual(response.status_code, 403)

    def test_admin_can_create_category(self):
        self.login('admin')
        response = self.post_json('/api/categories/', {'name': 'Гараж', 'slug': 'garage'})
        self.assertEqual(response.status_code, 201)
