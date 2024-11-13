from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from ads.models import Ad, Profile

class Chat(models.Model):
    ad = models.ForeignKey(Ad, related_name="chats", on_delete=models.CASCADE)
    buyer = models.ForeignKey(Profile, related_name="buyer_chats", on_delete=models.CASCADE)
    seller = models.ForeignKey(Profile, related_name="seller_chats", on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    def __str__(self):
        return f"Chat between {self.seller.user.username} and {self.buyer.user.username} for {self.ad.title}"

class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(Profile, related_name="sent_messages", on_delete=models.CASCADE)
    message = models.TextField(_("Message"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)  # Add this field

    def __str__(self):
        return f"Message from {self.sender.user.username} in chat with {self.chat.seller.user.username} for {self.chat.ad.title}"