from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ads.models import Ad, Category, Profile
from ad_chat.models import Chat

class ChatCreationTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='buyer', password='password')
        self.seller_user = get_user_model().objects.create_user(username='seller', password='password')
        self.buyer_profile = Profile.objects.create(user=self.user)
        self.seller_profile = Profile.objects.create(user=self.seller_user)
        self.category = Category.objects.create(name='ABC', type='ABC')
        self.ad = Ad.objects.create(
                    user=self.seller_profile,
                    category=self.category,
                    title='Title',
                    description='description',
                    location='location',
                    postal_code=12345,
                    contact_email='testuser@example.com',
                    contact_phone='1234567890',
                    show_contact=True
                )
        self.chat_url = reverse('ad_chat:chat_detail', kwargs={'chat_id': 1})
        self.client.login(username='buyer', password='password')

    def test_create_chat(self):
        """
        Test that a chat is created successfully between a buyer and seller
        """
        response = self.client.post(reverse('ad_chat:create_chat', kwargs={'ad_id': self.ad.id}))
        chat = Chat.objects.get(ad=self.ad, buyer=self.buyer_profile, seller=self.seller_profile)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(chat.buyer, self.buyer_profile)
        self.assertEqual(chat.seller, self.seller_profile)

    def test_create_chat_with_self(self):
        """
        Ensure a user cannot create a chat with themselves.
        """
        response = self.client.post(reverse('ad_chat:create_chat', kwargs={'ad_id': self.ad.id}), 
                                    {'user': self.seller_user})
        self.assertEqual(response.status_code, 302)

    def test_view_chat_forbidden(self):
        """
        Ensure a user cannot view a chat they are not a part of.
        """
        other_user = get_user_model().objects.create_user(username='another_user', password='password')
        self.client.login(username='another_user', password='password')
        response = self.client.get(self.chat_url)
        self.assertEqual(response.status_code, 404)

    def test_view_chat_for_authorized_user(self):
        """
        Ensure an authorized user (buyer or seller) can view the chat.
        """
        self.client.post(reverse('ad_chat:create_chat', kwargs={'ad_id': self.ad.id}))
        response = self.client.get(self.chat_url)
        self.assertEqual(response.status_code, 200)
        