from django.test import TestCase, Client
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.contrib.auth.models import User
from accounts.models import UserInfo
from accounts.forms import UserLoginForm, UserRegisterForm, UserUpdateForm
import uuid


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

    def test_invalid_register_form_username_exists(self):
        """
        Test an invalid form due to existing username
        """
        User.objects.create_user(
            username="TestRegisterUsernameExists", password="TestPassword")
        form_data = {
            "username": "TestRegisterUsernameExists",
            "password": "TestPassword",
            "v_password": "TestPassword",
            "email": "test@testserver.kryptedgaming.com",
            "country": "US",
            "age": 18,
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue("username" in form.errors)

    def test_invalid_register_form_email_exists(self):
        """
        Test an invalid form due to existing email
        """
        User.objects.create_user(username="TestRegisterEmailExists",
                                 email="TestRegister@test.com", password="TestPassword")
        form_data = {
            "username": "TestRegisterEmail",
            "password": "TestPassword",
            "v_password": "TestPassword",
            "email": "TestRegister@test.com",
            "country": "US",
            "age": 18,
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue("email" in form.errors)


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

    def test_invalid_login_form_user_does_not_exist(self):
        """
        Test an invalid form with a non-existent user
        """
        form_data = {
            "username": "TestNonexistentUser",
            "password": "TestPassword2",
        }
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue("username" in form.errors)

    def test_valid_login_form_inactive_user(self):
        """
        Test a valid form with an inactive user
        """
        User.objects.create_user(
            username="TestInactiveUser", password="TestPassword")
        user = User.objects.get(username="TestInactiveUser")
        user.is_active = False
        user.save()
        form_data = {
            "username": "TestInactiveUser",
            "password": "TestPassword",
        }
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue("username" in form.errors)


class UserUpdateFormTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="TestUser", password="TestPassword", email="Test@test.kryptedgaming.com")

        UserInfo(user=User.objects.get(username="TestUser"),
                 age="18", country="US").save()

    def test_valid_update_form(self):
        """
        Test a valid form
        """
        form_data = {
            "username": "",
            "email": "testupdate@test.kryptedgaming.com"
        }
        form = UserUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_update_form_existing_username(self):
        """
        Test an invalid form due to existing username
        """
        form_data = {
            "username": "TestUser",
            "email": ""
        }
        form = UserUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue("username" in form.errors)

    def test_invalid_update_form_existing_email(self):
        """
        Test an invalid form due to existing email
        """
        form_data = {
            "username": "",
            "email": "Test@test.kryptedgaming.com"
        }
        form = UserUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue("email" in form.errors)

    def test_invalid_update_form_username_spaces(self):
        """
        Test an invalid form due to spaces in username
        """
        form_data = {
            "username": "Test User",
            "email": ""
        }
        form = UserUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue("username" in form.errors)

    def test_invalid_update_form_username_symbols(self):
        """
        Test an invalid form due to @ in username
        """
        form_data = {
            "username": "Test@User",
            "email": ""
        }
        form = UserUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue("username" in form.errors)


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
        user = User.objects.get(username=register_form['username'])
        self.assertTrue(user)
        self.assertTrue(user.username == "TestRegister")
        self.assertTrue(user.email == "TestRegister@test.kryptedgaming.com")
        self.assertTrue(user.info.age == 18)
        self.assertTrue(user.info.country == "US")

    def test_register_success_email_disabled(self):
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

        settings.EMAIL_HOST = '1'
        response = self.client.post(url, register_form)
        user = User.objects.get(username=register_form['username'])
        self.assertTrue(user)
        self.assertTrue(user.username == "TestRegister")
        self.assertTrue(user.email == "TestRegister@test.kryptedgaming.com")
        self.assertTrue(user.info.age == 18)
        self.assertTrue(user.info.country == "US")


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

    def test_login_success_with_next(self):
        view_user_url = reverse('accounts-user', args=("TestUser",))

        login_form = {
            'username': "TestUser",
            'password': "TestPassword"
        }

        response = self.client.get(view_user_url)
        self.assertTrue(response.status_code == 302)
        url = response.url

        response = self.client.post(url, login_form)
        self.assertTrue(response.status_code == 302)
        self.assertTrue(response.url == view_user_url)


class UserViewTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="TestUser", password="TestPassword", email="test@test.com")

        UserInfo(user=User.objects.get(username="TestUser"),
                 age="18", country="US").save()

        User.objects.create_user(
            username="TestUserTwo", password="TestPassword", email="test2@test.com")

        UserInfo(user=User.objects.get(username="TestUserTwo"),
                 age="18", country="US").save()

    def test_get_user_success(self):
        self.client.login(username="TestUser", password="TestPassword")

        url = reverse('accounts-user', args=("TestUser",))
        response = self.client.get(url)

        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.context['user']
                        == User.objects.get(username="TestUser"))

    def test_get_user_failure(self):
        self.client.login(username="TestUser", password="TestPassword")

        url = reverse('accounts-user', args=("FakeTestUser",))
        response = self.client.get(url)

        self.assertTrue(response.status_code == 302)
        self.assertTrue(response.url == "/")

        response = self.client.get("/")
        self.assertTrue(response.context["messages"])

    def test_post_user_success_username(self):
        self.client.login(username="TestUser", password="TestPassword")
        url = reverse('accounts-user', args=("TestUser",))
        form_data = {
            "username": "TestUser2",
            "email": ""
        }
        response = self.client.post(url, form_data, follow=True)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.context['user'].username == "TestUser2")

    def test_post_user_success_email(self):
        self.client.login(username="TestUser",
                          email="test@test.com", password="TestPassword")
        url = reverse('accounts-user', args=("TestUser",))
        form_data = {
            "username": "",
            "email": "testvalid@test.com"
        }
        response = self.client.post(url, form_data, follow=True)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.context['user'].email == "testvalid@test.com")

    def test_post_user_failure_wrong_account(self):
        self.client.login(username="TestUser",
                          email="test@test.com", password="TestPassword")
        url = reverse('accounts-user', args=("TestUserTwo",))
        form_data = {
            "username": "",
            "email": "testinvalid@test.com"
        }
        response = self.client.post(url, form_data, follow=True)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.context['user'].email == "test2@test.com")
        self.assertFalse(
            response.context['user'].email == "testinvalid@test.com")

    def test_post_user_failure_invalid_form(self):
        self.client.login(username="TestUser",
                          email="test@test.com", password="TestPassword")
        url = reverse('accounts-user', args=("TestUser",))
        form_data = {
            "username": "Test@User",
            "email": ""
        }
        response = self.client.post(url, form_data, follow=True)
        self.assertTrue(str(list(response.context['messages'])[
                        0]) == "Failed to update account information.")

    def test_post_user_success_same_username(self):
        self.client.login(username="TestUser",
                          email="test@test.com", password="TestPassword")
        url = reverse('accounts-user', args=("TestUser",))
        form_data = {
            "username": "TestUser",
            "email": ""
        }
        response = self.client.post(url, form_data, follow=True)
        self.assertTrue(response.context['user'].username == "TestUser")

    def test_post_user_success_same_email(self):
        self.client.login(username="TestUser",
                          email="test@test.com", password="TestPassword")
        url = reverse('accounts-user', args=("TestUser",))
        form_data = {
            "username": "",
            "email": "test@test.com"
        }
        response = self.client.post(url, form_data, follow=True)
        self.assertTrue(response.context['user'].email == "test@test.com")


class UserDeleteViewTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="TestUser", password="TestPassword", email="Test@test.kryptedgaming.com")

        UserInfo(user=User.objects.get(username="TestUser"),
                 age="18", country="US").save()

        User.objects.create_user(
            username="TestUser2", password="TestPassword", email="Test2@test.kryptedgaming.com")

        UserInfo(user=User.objects.get(username="TestUser2"),
                 age="18", country="US").save()

    def test_delete_user_success(self):
        self.client.login(username="TestUser", password="TestPassword")

        url = reverse('accounts-user-delete',
                      args=(User.objects.get(username="TestUser").pk,))
        response = self.client.post(url)

        self.assertTrue(response.status_code == 302)
        self.assertFalse(User.objects.filter(username="TestUser").exists())

    def test_delete_user_failure(self):
        self.client.login(username="TestUser", password="TestPassword")

        url = reverse('accounts-user-delete',
                      args=(User.objects.get(username="TestUser2").pk,))
        response = self.client.post(url, follow=True)

        self.assertTrue(str(list(response.context['messages'])[
                        0]) == "Nice try, but that is not your account.")
        self.assertTrue(User.objects.filter(username="TestUser2").exists())


class UserActivateTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="TestUser", password="TestPassword", email="Test@test.kryptedgaming.com")

        UserInfo(user=User.objects.get(username="TestUser"),
                 age="18", country="US").save()

        user = User.objects.get(username="TestUser")
        user.is_active = False
        user.save()

    def test_success_account_activation(self):
        user = User.objects.get(username="TestUser")
        url = reverse('accounts-activate', args=(user.info.secret,))

        self.assertFalse(user.is_active)
        response = self.client.get(url)
        user = User.objects.get(username="TestUser")
        self.assertTrue(user.is_active)

    def test_failure_account_activation(self):
        url = reverse('accounts-activate', args=(uuid.uuid4(),))

        response = self.client.get(url, follow=True)
        self.assertTrue(str(list(response.context['messages'])[
                        0]) == "Unable to activate account. Contact support.")
