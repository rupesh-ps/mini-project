from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from ..models import Profile, Category, Ad
from ..views import AdCreateView, AdUpdateView, AdDeleteView

User = get_user_model()

class InitialSetup(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user, phone='1234567890', email='testuser@example.com')
        self.category_job = Category.objects.create(name='Job', type='job')
        self.category_sale = Category.objects.create(name='Sale', type='sale')
        self.client.login(username='testuser', password='testpassword')

class AdCreateViewTest(InitialSetup):
    def setUp(self):
        super().setUp()
        self.category_job = Category.objects.create(name='Job', type='job')
        self.category_sale = Category.objects.create(name='Sale', type='sale')
        self.url = reverse('ad-create')
        self.client.login(username='testuser', password='testpassword')
        self.response = self.client.get(self.url)

    def test_ad_create_view_success_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_ad_create_view_url_resolves_correct_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func.view_class, AdCreateView)

    def test_ad_create_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'ads/ad_create.html')

    def test_ad_create_view_form_valid(self):
        data = {
            'category': self.category_job.id,
            'title': 'Test Job Ad',
            'description': 'Test description for job ad',
            'tags': 'test, job',
            'price': 100,
            'location': 'Test location',
            'postal_code': 12345,
            'contact_email': 'testuser@example.com',
            'contact_phone': '1234567890',
            'show_contact': True
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)

    def test_ad_create_view_form_invalid(self):
        data = {
            'category': self.category_job.id,
            'title': 'Test Invalid Ad',
            'description': '',
            'tags': '',
            'price': '',
            'location': '',
            'postal_code': 12345,
            'contact_email': '',
            'contact_phone': '',
            'show_contact': True
        }
        response = self.client.post(self.url, data)
        form = response.context.get('form')
        self.assertFalse(form.is_valid())

class AdUpdateViewTest(InitialSetup):
    def setUp(self):
        super().setUp()
        self.category_job = Category.objects.create(name='Job', type='job')
        self.category_sale = Category.objects.create(name='Sale', type='sale')
        self.ad = Ad.objects.create(
            user=self.profile,
            category=self.category_job,
            title='Old Title',
            description='Old description',
            location='Old location',
            postal_code=12345,
            contact_email='testuser@example.com',
            contact_phone='1234567890',
            show_contact=True
        )
        self.url = reverse('ad-update', kwargs={'pk': self.ad.pk})
        self.client.login(username='testuser', password='testpassword')
        self.response = self.client.get(self.url)

    def test_ad_update_view_success_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_ad_update_view_url_resolves_correct_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func.view_class, AdUpdateView)

    def test_ad_update_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'ads/ad_update.html')

    def test_ad_update_view_form_valid(self):
        data = {
            'category': self.category_sale.id,
            'title': 'Updated Ad Title',
            'description': 'Updated description',
            'tags': 'test, updated',
            'price': 100.00,
            'location': 'Updated location',
            'postal_code': 54321,
            'contact_email': 'updated@example.com',
            'contact_phone': '9876543210',
            'show_contact': True
        }

        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.ad.refresh_from_db()
        self.assertEqual(self.ad.title, 'Updated Ad Title')
        self.assertEqual(self.ad.location, 'Updated location')

class AdDeleteViewTest(InitialSetup):
    def setUp(self):
        super().setUp()
        self.ad = Ad.objects.create(
            user=self.profile,
            category=self.category_job,
            title='Ad to Delete',
            description='Description for delete test',
            location='Test location',
            postal_code=12345
        )
        self.url = reverse('ad-delete', args=[self.ad.id])
        self.client.login(username='testuser', password='testpassword')
        self.response = self.client.get(self.url)

    def test_ad_delete_view_success_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_ad_delete_view_url_resolves_correct_view(self):
        view = resolve(self.url)
        self.assertEqual(view.func.view_class, AdDeleteView)

    def test_ad_delete_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'ads/ad_delete.html')

    def test_ad_delete_view_contains_navigation_links(self):
        ad_list_url = reverse('ad-list')
        self.assertContains(self.response, f'href="{ad_list_url}"')

    def test_ad_delete_view_post_delete(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Ad.objects.filter(id=self.ad.id).exists())

class ProfileViewTest(InitialSetup):
    def setUp(self):
        super().setUp()
        self.url = reverse('profile')
        self.client.login(username='testuser', password='testpassword')
        self.response = self.client.get(self.url)

    def test_profile_view_success_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_profile_view_contains_user_info(self):
        self.assertContains(self.response, 'testuser')
        self.assertContains(self.response, self.profile.phone)

class ProfileEditViewTest(InitialSetup):
    def setUp(self):
        super().setUp()
        self.url = reverse('profile-edit')
        self.client.login(username='testuser', password='testpassword')

    def test_profile_edit_view_success_code(self):
        data = {
            'phone': '9876543210',
            'email': 'updateduser@example.com'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.phone, '9876543210')
        self.assertEqual(self.profile.email, 'updateduser@example.com')
