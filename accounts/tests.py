from django.test import TestCase
from django.test import TestCase, Client
from django.db.utils import IntegrityError
from django.urls import reverse
from .models import CustomUser, Profile


class UserModelTest(TestCase):
    def setUp(self):
        """
        Set up the necessary objects for the test cases.
        """
        self.user = CustomUser.objects.create_user(email="test@gmail.com", password="password", name="Test")

    def test_create_user(self):
        """
        Test creating a user.
        """
        # Test creating a user with valid data
        created_user = CustomUser.objects.get(email="test@gmail.com")
        self.assertEqual(created_user, self.user)

        # Attempt to create user with already taken email, should raise IntegrityError
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(email="test@gmail.com", password="password", name="Test2")

        # Attempt to create user with missing email, should raise ValueError
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email="", password="password", name="Test3")

    def test_create_superuser(self):
        """
        Test creating a superuser.
        """
        superuser = CustomUser.objects.create_superuser(email="admin@gmail.com", password="adminpassword")
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_profile_creation(self):
        """
        Test creating a profile.
        """
        # Delete any existing profiles associated with the user
        Profile.objects.filter(user=self.user).delete()
        profile = Profile.objects.create(user=self.user, profile_image='profile_images/profile_pic.jpg')
        self.assertEqual(profile.user, self.user)


class AccountsViewsTest(TestCase):
    def setUp(self) -> None:
        """
        Set up the test environment.
        """
        self.c = Client()
        # Create test user
        self.register_url = reverse("accounts:register")
        self.user_data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password1': 'test123!',
            'password2': 'test123!'
        }
        self.response = self.c.post(self.register_url, data=self.user_data)
        self.user = CustomUser.objects.get(email=self.user_data['email'])

    def test_registration_request(self):
        """
        Test registration request.
        """
        # Check if the user is redirected
        self.assertEqual(self.response.status_code, 302)
        # Check if the redirected URL is correct
        self.assertRedirects(self.response, reverse('products:product_list'))
        # Check if the user is created and saved in the database
        self.user = CustomUser.objects.get(email=self.user_data["email"])
        self.assertEqual(self.user_data["email"], self.user.email)

    def test_login_request(self):
        """
        Test login request.
        """
        login_user = {
            'username': self.user_data['email'], 
            'password': self.user_data['password1']
        }
        login_url = reverse("accounts:login")
        response = self.c.post(login_url, data=login_user)

        # Check if the user is redirected
        self.assertEqual(response.status_code, 302)
        # Check if the redirected URL is correct
        self.assertRedirects(response, reverse('products:product_list'))

    def test_logout(self):
        """
        Test logout request.
        """
        # Authenticate the user using force_login
        self.c.force_login(self.user)

        # Make a GET request to the logout URL
        logout_url = reverse("accounts:logout")
        response = self.c.get(logout_url)

        # Check if the user is redirected
        self.assertEqual(response.status_code, 302)
        # Check if the redirected URL is correct (e.g., redirect to homepage)
        self.assertRedirects(response, reverse('products:product_list'))
    
    def test_profile_request(self):
        """
        Test profile request.
        """
        # Authenticate the user using force_login
        self.c.force_login(self.user)
        profile_url = reverse("accounts:profile")
        response = self.c.get(profile_url)
        self.assertEqual(response.status_code, 200)
        # Check if the correct template is used for rendering
        self.assertTemplateUsed(response, 'profile.html')
        # Check if content in response is correct
        self.assertContains(response, self.user.email)

    def test_edit_profile_request(self):
        """
        Test edit profile request.
        """
        self.c.force_login(self.user)
        edit_profile_url = reverse("accounts:edit_profile")
        response = self.c.post(edit_profile_url, {"name": "Updated Name", "email":"updatedemail@gmail.com"})
        self.assertEqual(response.status_code, 200)
        updated_user = CustomUser.objects.get(email="updatedemail@gmail.com")
        self.assertEqual(updated_user.name, 'Updated Name')

    def test_change_password_request(self):
        """
        Test change password request.
        """
        change_password_url = reverse("accounts:password_change")
        data = {
            'old_password': self.user_data["password1"],
            'new_password1': "newPassword1",
            'new_password2': "newPassword1",
        }
        response = self.client.post(change_password_url, data)
        self.assertEqual(response.status_code, 302)
