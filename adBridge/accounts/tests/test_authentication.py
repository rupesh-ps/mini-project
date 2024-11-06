from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from django.contrib.auth import get_user_model

class UserAuthTests(TestCase):

    def setUp(self):
        """Set up initial data for tests."""
        
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.password_reset_url = reverse('reset_password')
        self.password_reset_done_url = reverse('password_reset_done')
        self.password_reset_complete_url = reverse('password_reset_complete')
        self.homepage_url = reverse('homepage')

        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
        }
        self.user = User.objects.create_user(**self.user_data)
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        
    def test_signup_page_access(self):
        """Test that the signup page is accessible."""

        self.client.logout()
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_signup_form_valid(self):
        """Test signing up a new user."""
        self.client.logout()
        signup_user_data = {
            'username': 'testuser_signup',  
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123', 
        }
        response = self.client.post(self.signup_url, signup_user_data)
        self.assertRedirects(response, self.login_url)

    def test_login_page_access(self):
        """Test that the login page is accessible."""
        self.client.logout()
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_form_valid(self):
        """Test logging in with correct credentials."""
        
        response = self.client.post(self.login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        self.assertRedirects(response, self.homepage_url)

    def test_login_redirects_when_logged_in(self):
        """Test that a logged-in user is redirected to the homepage when accessing the login page."""
        
        response = self.client.get(self.login_url)
        self.assertRedirects(response, self.homepage_url)

    def test_password_reset_page_access(self):
        """Test that the password reset page is accessible."""
        
        response = self.client.get(self.password_reset_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset.html')

    def test_password_reset_send_email(self):
        """Test that password reset email is sent."""
        
        response = self.client.post(self.password_reset_url, {'email': self.user_data['email']})
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.user_data['email'], mail.outbox[0].to)

    def test_password_reset_done_page_access(self):
        """Test that the password reset done page is accessible after request."""
        
        response = self.client.get(self.password_reset_done_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset_done.html')

    def test_password_reset_complete_page_access(self):
        """Test that the password reset complete page is accessible after completing reset."""
        
        response = self.client.get(self.password_reset_complete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset_complete.html')

    def test_logout_redirects_to_homepage(self):
        """Test that logging out redirects to the homepage."""
        
        response = self.client.post(self.logout_url)
        self.assertRedirects(response, self.homepage_url)

    def test_authenticated_user_redirects(self):
        """Test that an authenticated user cannot access login/signup."""
        

        response = self.client.get(self.login_url)
        self.assertRedirects(response, self.homepage_url)

        response = self.client.get(self.signup_url)
        self.assertRedirects(response, self.homepage_url)

    def test_authenticated_user_access_to_homepage(self):
        """Test that a logged-in user can access the homepage."""
        
        response = self.client.get(self.homepage_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

