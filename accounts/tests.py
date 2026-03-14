from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class AccountViewsTestCase(TestCase):

    def test_register_view_get(self):
        """Test register view renders form on GET."""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Register')

    def test_register_view_post_valid(self):
        """Test successful user registration."""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        response = self.client.post(reverse('register'), data)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_view_post_duplicate_username(self):
        """Test registration fails with duplicate username."""
        User.objects.create_user(username='existing', email='existing@example.com', password='pass')
        data = {
            'username': 'existing',
            'email': 'new@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)  # Form re-renders
        self.assertContains(response, 'A user with that username already exists')

    def test_login_view_get(self):
        """Test login view renders form on GET."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')

    def test_login_view_post_valid(self):
        """Test successful login."""
        user = User.objects.create_user(username='testuser', password='testpass')
        data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post(reverse('login'), data)
        self.assertRedirects(response, reverse('home'))

    def test_login_view_post_invalid(self):
        """Test login fails with invalid credentials."""
        data = {'username': 'nonexistent', 'password': 'wrong'}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct username and password')

    def test_logout_view(self):
        """Test user logout."""
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'))
