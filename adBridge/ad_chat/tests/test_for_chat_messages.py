from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ads.models import Ad, Category, Profile
from ad_chat.models import Chat, ChatMessage
from django.utils import timezone
from datetime import timedelta

class ChatMessageTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='buyer', password='password')
        self.seller_user = get_user_model().objects.create_user(username='seller', password='password')
        self.buyer_profile = Profile.objects.create(user=self.user)
        self.seller_profile = Profile.objects.create(user=self.seller_user)
        self.category = Category.objects.create(name='ABC', type='ABC')
        self.ad = Ad.objects.create(user=self.seller_profile, category=self.category, title='Title', description='description', location='location', postal_code=12345)
        self.chat = Chat.objects.create(ad=self.ad, buyer=self.buyer_profile, seller=self.seller_profile)
        self.chat_url = reverse('ad_chat:chat_detail', kwargs={'chat_id': self.chat.id})

    def test_send_message(self):
        """
        Ensure a user can send a message in a chat.
        """
        self.client.login(username='buyer', password='password')
        message_data = {'message': 'Hello, I am interested in this ad.'}
        response = self.client.post(self.chat_url, message_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ChatMessage.objects.count(), 1)
        message = ChatMessage.objects.first()
        self.assertEqual(message.message, 'Hello, I am interested in this ad.')
        self.assertEqual(message.sender, self.buyer_profile)

    def test_edit_message_within_time(self):
        """
        Ensure that a user can edit their message within 2 minutes.
        """
        self.client.login(username='buyer', password='password')
        message_data = {'message': 'Hello!'}
        self.client.post(self.chat_url, message_data)

        message = ChatMessage.objects.first()
        message_id = message.id
        updated_message_data = {'message': 'Hello, I have a question!'}
        url = reverse('ad_chat:chat_detail', kwargs={'chat_id': self.chat.id})

        response = self.client.post(url, {'message': 'Hello, I have a question!', 'message_id': message_id})
        message.refresh_from_db()
        self.assertEqual(message.message, 'Hello, I have a question!')
        self.assertEqual(response.status_code, 302)

    def test_edit_message_after_time_limit(self):
        """
        Ensure that a user cannot edit a message after 2 minutes.
        """
        self.client.login(username='buyer', password='password')
        message_data = {'message': 'Hello!'}
        self.client.post(self.chat_url, message_data)

        message = ChatMessage.objects.first()
        message.created_at = timezone.now() - timedelta(minutes=3)
        message.save()

        url = reverse('ad_chat:chat_detail', kwargs={'chat_id': self.chat.id})
        response = self.client.post(url, {'message': 'Updated message', 'message_id': message.id})
        self.assertEqual(response.status_code, 302)
