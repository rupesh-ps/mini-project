from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ads.models import Ad, Category, Profile
from ad_chat.models import Chat

class SellerInboxTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='buyer', password='password')
        self.seller_user = get_user_model().objects.create_user(username='seller', password='password')
        self.buyer_profile = Profile.objects.create(user=self.user)
        self.seller_profile = Profile.objects.create(user=self.seller_user)
        self.category = Category.objects.create(name='ABC', type='ABC')
        self.ad = Ad.objects.create(user=self.seller_profile, category=self.category, title='Title', description='description', location='location', postal_code=12345)
        self.chat = Chat.objects.create(ad=self.ad, buyer=self.buyer_profile, seller=self.seller_profile)

    def test_seller_inbox(self):
        """
        Ensure that a seller can see all their chats in the inbox.
        """
        self.client.login(username='seller', password='password')
        response = self.client.get(reverse('ad_chat:seller_inbox'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.chat.ad.title)