from django.test import TestCase
from django.contrib.auth.models import User
from ads.models import Profile, Ad, Category
from ad_chat.models import Chat, ChatMessage

class ChatModelTest(TestCase):

    def setUp(self):
        self.seller_user = User.objects.create_user(username='seller', password='password')
        self.buyer_user = User.objects.create_user(username='buyer', password='password')
        
        self.seller_profile = Profile.objects.create(user=self.seller_user, phone='1234567890', email='seller@example.com')
        self.buyer_profile = Profile.objects.create(user=self.buyer_user, phone='0987654321', email='buyer@example.com')
        self.category = Category.objects.create(name='ABC', type='ABC')

        self.ad = Ad.objects.create(
            user=self.seller_profile,
            category=self.category,
            title='Test Ad',
            location='Test Location',
            postal_code=12345,
            description='Test description'
        )
        
    def test_chat_creation(self):
        """
        Test chat creation
        """
        chat = Chat.objects.create(
            ad=self.ad,
            buyer=self.buyer_profile,
            seller=self.seller_profile
        )
        
        self.assertIsInstance(chat, Chat)
        self.assertEqual(chat.buyer, self.buyer_profile)
        self.assertEqual(chat.seller, self.seller_profile)
        self.assertEqual(chat.ad, self.ad)
        self.assertIsNotNone(chat.created_at)
        self.assertIsNotNone(chat.updated_at)

    def test_chat_str(self):
        """
        Test chat string representation
        """
        chat = Chat.objects.create(
            ad=self.ad,
            buyer=self.buyer_profile,
            seller=self.seller_profile
        )
        self.assertEqual(str(chat), f"Chat between {self.seller_user.username} and {self.buyer_user.username} for {self.ad.title}")


class ChatMessageModelTest(TestCase):

    def setUp(self):
        self.seller_user = User.objects.create_user(username='seller', password='password')
        self.buyer_user = User.objects.create_user(username='buyer', password='password')
        
        self.seller_profile = Profile.objects.create(user=self.seller_user, phone='1234567890', email='seller@example.com')
        self.buyer_profile = Profile.objects.create(user=self.buyer_user, phone='0987654321', email='buyer@example.com')
        self.category = Category.objects.create(name='ABC', type='ABC')

        self.ad = Ad.objects.create(
            user=self.seller_profile,
            category=self.category,
            title='Test Ad',
            location='Test Location',
            postal_code=12345,
            description='Test description'
        )
        
        self.chat = Chat.objects.create(
            ad=self.ad,
            buyer=self.buyer_profile,
            seller=self.seller_profile
        )

    def test_chat_message_creation(self):
        """
        Test chat message creation
        """
        message = ChatMessage.objects.create(
            chat=self.chat,
            sender=self.buyer_profile,
            message="Hello, I am interested in this ad."
        )
        
        self.assertIsInstance(message, ChatMessage)
        self.assertEqual(message.chat, self.chat)
        self.assertEqual(message.sender, self.buyer_profile)
        self.assertEqual(message.message, "Hello, I am interested in this ad.")
        self.assertIsNotNone(message.created_at)
        self.assertIsNotNone(message.updated_at)

    def test_chat_message_str(self):
        """
        Test chat message string representation
        """
        message = ChatMessage.objects.create(
            chat=self.chat,
            sender=self.buyer_profile,
            message="Hello, I am interested in this ad."
        )
        self.assertEqual(str(message), f"Message from {self.buyer_user.username} in chat with {self.seller_user.username} for {self.ad.title}")

    def test_message_timestamps(self):
        """
        Test chat message timestamps
        """
        message = ChatMessage.objects.create(
            chat=self.chat,
            sender=self.buyer_profile,
            message="Test message"
        )
        
        self.assertIsNotNone(message.created_at)
        self.assertIsNotNone(message.updated_at)

    def test_chat_message_relationship(self):
        """
        Test chat message relationships
        """
        message1 = ChatMessage.objects.create(
            chat=self.chat,
            sender=self.buyer_profile,
            message="Message 1"
        )
        message2 = ChatMessage.objects.create(
            chat=self.chat,
            sender=self.seller_profile,
            message="Message 2"
        )
        
        self.assertIn(message1, self.chat.messages.all())
        self.assertIn(message2, self.chat.messages.all())
