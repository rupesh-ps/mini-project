from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Profile, Category, Ad, Message

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test123')
        self.profile = Profile.objects.create(user=self.user, phone='1234567890', email='testuser@example.com')

    def test_profile(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.phone, '1234567890')
        self.assertEqual(self.profile.email, 'testuser@example.com')

    def test_profile_str(self):
        self.assertEqual(str(self.profile), 'testuser')


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Job Category', type='job')

    def test_category(self):
        self.assertEqual(self.category.name, 'Test Job Category')
        self.assertEqual(self.category.type, 'job')

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Test Job Category')
    
class AdModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test123')
        self.profile = Profile.objects.create(user=self.user, phone="1234567890", email="testuser@example.com")
        self.category = Category.objects.create(name='Category xyz', type='job')
        self.ad = Ad.objects.create(user=self.profile,
                                    category=self.category,
                                    title='Test Ad Title',
                                    image='test_image.jpg',
                                    tags = ['test'],
                                    location='Test Location', 
                                    postal_code=12345, 
                                    description='Test Ad Description', 
                                    show_contact=True, 
                                    price=100.00, 
                                    contact_email='testuser@example.com', 
                                    contact_phone='1234567890',
                                    posted_at='2021-01-01 12:00:00')

    def test_ad_creation_success(self):

        self.assertEqual(self.ad.user, self.profile)
        self.assertEqual(self.ad.category, self.category)
        self.assertEqual(self.ad.title, 'Test Ad Title')
        self.assertEqual(self.ad.price, 100.00)

    def test_price_required_for_sale_ads(self):
        sale_category = Category.objects.create(name='Sale Category', type='sale')
        sale_ad = Ad(user=self.profile, category=sale_category, title='Test Sale Ad', price=None)
        with self.assertRaises(ValueError):
            sale_ad.save()

    def test_contact_email_and_phone_required_for_job_ads(self):
        job_category = Category.objects.create(name='Job Category', type='job')
        job_ad = Ad(user=self.profile, category=job_category, title='Test Job Ad')
        with self.assertRaises(ValueError):
            job_ad.save()

    def test_ad_str(self):
        self.assertEqual(str(self.ad), 'Test Ad Title (Category xyz)')

class MessageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test123')
        self.profile = Profile.objects.create(user=self.user, phone="1234567890", email="testuser@example.com")
        self.category = Category.objects.create(name='Test Job Category', type='job')
        self.ad = Ad.objects.create(user=self.profile,
                                    category=self.category,
                                    title='Test Ad Title',
                                    image='test_image.jpg',
                                    tags = ['test'],
                                    location='Test Location', 
                                    postal_code=12345, 
                                    description='Test Ad Description', 
                                    show_contact=True, 
                                    price=100.00,
                                    contact_email='testuser@example.com', 
                                    contact_phone='1234567890',
                                    posted_at='2021-01-01 12:00:00')
        self.message = Message.objects.create(ad=self.ad, message='Test Message', sender_email='testuser@example.com')

    def test_message_ad_relation(self):
        self.message = Message.objects.create(ad=self.ad, message='Test Message', sender_email='testuser@example.com')
        self.assertEqual(self.message.ad, self.ad)

    def test_message_str(self):
        self.assertEqual(str(self.message), 'Message from testuser@example.com regarding Test Ad Title')


