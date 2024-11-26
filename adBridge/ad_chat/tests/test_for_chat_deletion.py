from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ads.models import Ad, Category, Profile
from ad_chat.models import Chat, ChatMessage

class ChatMessageDeletionTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='buyer', password='password')
        self.seller_user = get_user_model().objects.create_user(username='seller', password='password')
        self.buyer_profile = Profile.objects.create(user=self.user)
        self.seller_profile = Profile.objects.create(user=self.seller_user)
        self.category = Category.objects.create(name='ABC', type='ABC')
        self.ad = Ad.objects.create(user=self.seller_profile, category=self.category, title='Title', description='description', location='location', postal_code=12345)
        self.chat = Chat.objects.create(ad=self.ad, buyer=self.buyer_profile, seller=self.seller_profile)
        self.chat_url = reverse('ad_chat:chat_detail', kwargs={'chat_id': self.chat.id})

    def test_delete_message(self):
        """
        Ensure that a user can delete their own message.
        """
        self.client.login(username='buyer', password='password')
        message_data = {'message': 'Hello!'}
        self.client.post(self.chat_url, message_data)

        message = ChatMessage.objects.first()
        message_id = message.id
        response = self.client.post(self.chat_url, {'delete_message': message_id})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(ChatMessage.objects.count(), 0)

    def test_delete_others_message(self):
        """
        Ensure a user cannot delete another user's message.
        """
        self.client.login(username='seller', password='password')
        message_data = {'message': 'Hello!'}
        self.client.post(self.chat_url, message_data)

        message = ChatMessage.objects.first()
        self.client.logout()
        self.client.login(username='buyer', password='password')
        response = self.client.post(self.chat_url, {'delete_message': message.id})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(ChatMessage.objects.count(), 1)
