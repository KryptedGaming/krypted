from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from accounts.models import UserInfo
from accounts.forms import UserLoginForm, UserRegisterForm, UserUpdateForm


class UserRegisterFormTestCase(TestCase):
    def test_valid_register_form(self):
        """
        Test a valid form with standard input.
        """
        form_data = {
            "username": "TestUser",
            "password": "TestPassword",
            "v_password": "TestPassword",
            "email": "test@testserver.kryptedgaming.com",
            "country": "US",
            "age": 18,
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_register_form_age(self):
        """
        Test an invalid form due to underage user
        """
        form_data = {
            "username": "TestUser",
            "password": "TestPassword",
            "v_password": "TestPassword",
            "email": "test@testserver.kryptedgaming.com",
            "country": "US",
            "age": 17,
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue("age" in form.errors)

    def test_invalid_register_form_username_length(self):
        """
        Test an invalid form due to improper username length
        """
        form_data = {
            "username": "Te",
            "password": "TestPassword",
            "v_password": "TestPassword",
            "email": "test@testserver.kryptedgaming.com",
            "country": "US",
            "age": 18,
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue("username" in form.errors)

    def test_invalid_register_form_username_space(self):
        """
        Test an invalid form due to spaces in username
        """
        form_data = {
            "username": "Test User",
            "password": "TestPassword",
            "v_password": "TestPassword",
            "email": "test@testserver.kryptedgaming.com",
            "country": "US",
            "age": 18,
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue("username" in form.errors)

    def test_invalid_register_form_username_symbol(self):
        """
        Test an invalid form due to @ in username
        """
        form_data = {
            "username": "Test@User",
            "password": "TestPassword",
            "v_password": "TestPassword",
            "email": "test@testserver.kryptedgaming.com",
            "country": "US",
            "age": 18,
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue("username" in form.errors)

    def test_invalid_register_form_mismatched_passwords(self):
        """
        Test an invalid form due to mismatched passwords
        """
        form_data = {
            "username": "TestUser",
            "password": "TestPassword",
            "v_password": "TestPassword2",
            "email": "test@testserver.kryptedgaming.com",
            "country": "US",
            "age": 18,
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue("password" in form.errors)


class UserLoginFormTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="TestUser", password="TestPassword", email="Test@test.kryptedgaming.com")

        UserInfo(user=User.objects.get(username="TestUser"),
                 age="18", country="US").save()

    def test_valid_login_form(self):
        """
        Test a valid form with standard input
        """
        form_data = {
            "username": "TestUser",
            "password": "TestPassword",
        }
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_login_form_email(self):
        """
        Test a valid form with an email instead of a username
        """
        form_data = {
            "username": "Test@test.kryptedgaming.com",
            "password": "TestPassword",
        }
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_login_form_password(self):
        """
        Test an invalid form with an incorrect password
        """
        form_data = {
            "username": "Test@test.kryptedgaming.com",
            "password": "TestPassword2",
        }
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue("password" in form.errors)


class UserRegisterViewTestcase(TestCase):
    def test_register_success(self):
        url = reverse_lazy('accounts-register')

        register_form = {
            'username': 'TestRegister',
            'email': 'TestRegister@test.kryptedgaming.com',
            'password': 'TestPassword1',
            'v_password': 'TestPassword1',
            'age': 18,
            'country': "US"
        }

        response = self.client.get(url)
        self.assertTrue(response.status_code == 200)

        response = self.client.post(url, register_form)
        self.assertTrue(User.objects.filter(
            username=register_form['username']).exists())


class UserLoginViewTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="TestUser", password="TestPassword", email="Test@test.kryptedgaming.com")

        UserInfo(user=User.objects.get(username="TestUser"),
                 age="18", country="US").save()

    def test_login_success(self):
        url = reverse_lazy('accounts-login')

        login_form = {
            'username': "TestUser",
            'password': "TestPassword"
        }

        response = self.client.get(url)
        self.assertTrue(response.status_code == 200)

        response = self.client.post(url, login_form)
        self.assertTrue(response.status_code == 302)
        self.assertTrue(response.url == "/")
