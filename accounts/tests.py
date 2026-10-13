from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import Profile


class AccountsTests(TestCase):
    """
    Test suite for user registration, authentication, profile management, and authorization.
    """

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.profile_edit_url = reverse('profile_edit')

        # Test user
        self.user1 = User.objects.create_user(
            username='userone',
            email='userone@example.com',
            password='password123',
            first_name='User',
            last_name='One'
        )

    def test_user_registration_success(self):
        """Test successful registration and profile creation."""
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        # Should redirect to feed
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        # Profile should be auto-created via signal
        new_user = User.objects.get(username='newuser')
        self.assertTrue(hasattr(new_user, 'profile'))
        self.assertEqual(new_user.profile.user, new_user)

    def test_user_registration_password_mismatch(self):
        """Test registration failure when passwords do not match."""
        response = self.client.post(self.register_url, {
            'username': 'mismatchuser',
            'email': 'mismatch@example.com',
            'password': 'password123',
            'confirm_password': 'different_password'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='mismatchuser').exists())
        self.assertFormError(response.context['form'], 'confirm_password', "Passwords do not match. Please verify and try again.")

    def test_user_registration_duplicate_username(self):
        """Test registration failure with already taken username."""
        response = self.client.post(self.register_url, {
            'username': 'userone',
            'email': 'another@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'username', "A user with that username already exists. Please pick another.")

    def test_user_login_and_logout(self):
        """Test login with valid credentials and logout."""
        # Login
        response = self.client.post(self.login_url, {
            'username': 'userone',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('feed'))

        # Check authenticated state
        self.assertTrue('_auth_user_id' in self.client.session)

        # Logout
        logout_response = self.client.get(self.logout_url)
        self.assertEqual(logout_response.status_code, 302)
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_user_invalid_login(self):
        """Test login with incorrect password."""
        response = self.client.post(self.login_url, {
            'username': 'userone',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_view_public_profile(self):
        """Test viewing public profile of a user."""
        profile_url = reverse('profile', kwargs={'username': self.user1.username})
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user1.username)
        self.assertContains(response, self.user1.profile.display_name)

    def test_profile_edit_authenticated(self):
        """Test that logged-in user can update their profile."""
        self.client.login(username='userone', password='password123')
        response = self.client.post(self.profile_edit_url, {
            'first_name': 'UpdatedFirst',
            'last_name': 'UpdatedLast',
            'email': 'updated@example.com',
            'bio': 'My updated bio description'
        })
        self.assertEqual(response.status_code, 302)
        self.user1.refresh_from_db()
        self.user1.profile.refresh_from_db()
        self.assertEqual(self.user1.first_name, 'UpdatedFirst')
        self.assertEqual(self.user1.email, 'updated@example.com')
        self.assertEqual(self.user1.profile.bio, 'My updated bio description')

    def test_profile_edit_unauthenticated_redirect(self):
        """Test that unauthenticated user is redirected to login when accessing profile edit."""
        response = self.client.get(self.profile_edit_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(reverse('login') in response.url)
