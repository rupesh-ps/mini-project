from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Chat, ChatMessage
from ads.models import Ad, Profile

class CreateChatView(LoginRequiredMixin, View):
    def get(self, request, ad_id):
        ad = get_object_or_404(Ad, id=ad_id)
        buyer = get_object_or_404(Profile, user=request.user)

        if ad.user == buyer:
            messages.error(request, 'You cannot chat with yourself.')
            return redirect('ad-detail', pk=ad.id)

        seller = ad.user
        chat, created = Chat.objects.get_or_create(ad=ad, buyer=buyer, seller=seller)

        if created:
            messages.success(request, 'Chat created successfully.')
        else:
            messages.info(request, 'Chat already exists.')

        return redirect('ad_chat:chat_detail', chat_id=chat.id)

class ChatDetailView(LoginRequiredMixin, View):
    def get(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id)

        if not self.is_user_in_chat(chat, request.user):
            messages.error(request, 'You are not authorized to view this chat.')
            return redirect('homepage')

        messages_in_chat = ChatMessage.objects.filter(chat=chat).order_by('created_at')

        for message in messages_in_chat:
            self.set_message_permissions(message, request)

        return render(request, 'ad_chat/chat.html', {
            'chat': chat,
            'messages': messages_in_chat,
        })

    def post(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id)

        if not self.is_user_in_chat(chat, request.user):
            messages.error(request, 'You are not authorized to perform this action.')
            return redirect('home')

        message_text = request.POST.get('message')
        message_id = request.POST.get('message_id')

        if message_text:
            if message_id:
                return self.handle_message_update(request, message_id, message_text)
            else:
                return self.send_new_message(request, message_text, chat)
        elif 'delete_message' in request.POST:
            message_id = request.POST.get('delete_message')
            return self.handle_message_delete(request, message_id)

        return redirect('ad_chat:chat_detail', chat_id=chat.id)

    def handle_message_update(self, request, message_id, message_text):
        message = get_object_or_404(ChatMessage, id=message_id)
        if self.update_message(message, message_text, request.user):
            messages.success(request, 'Message updated successfully.')
        else:
            messages.error(request, 'You can only edit your messages within 2 minutes of sending.')

        return redirect('ad_chat:chat_detail', chat_id=message.chat.id)

    def handle_message_delete(self, request, message_id):
        message = get_object_or_404(ChatMessage, id=message_id)
        if self.delete_message(message, request.user):
            messages.success(request, 'Message deleted successfully.')
        else:
            messages.error(request, 'You can only delete your own messages.')

        return redirect('ad_chat:chat_detail', chat_id=message.chat.id)

    def send_new_message(self, request, message_text, chat):
        sender = chat.buyer if chat.buyer.user == request.user else chat.seller
        ChatMessage.objects.create(chat=chat, sender=sender, message=message_text)
        messages.success(request, 'Message sent successfully.')
        return redirect('ad_chat:chat_detail', chat_id=chat.id)

    def update_message(self, message, new_text, user):
        if self.can_edit(message, user):
            message.message = new_text
            message.updated_at = timezone.now()
            message.save()
            return True
        return False

    def delete_message(self, message, user):
        if self.can_delete(message, user):
            message.delete()
            return True
        return False

    def can_edit(self, message, user):
        return message.sender.user == user and (timezone.now() - message.created_at <= timedelta(minutes=2))

    def can_delete(self, message, user):
        return message.sender.user == user

    def set_message_permissions(self, message, request):
        message.can_edit = self.can_edit(message, request.user)
        message.can_delete = self.can_delete(message, request.user)

    def is_user_in_chat(self, chat, user):
        return chat.buyer.user == user or chat.seller.user == user

class InboxView(View):
    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        chats = Chat.objects.filter(seller=profile).order_by('-created_at')

        return render(request, 'ad_chat/inbox.html', {
            'chats': chats,
        })

class NewMessageView(View):
    def get(self, request):
        user_profile = get_object_or_404(Profile, user=request.user)
        ads = Ad.objects.exclude(user=user_profile)
        return render(request, 'ad_chat/new_message.html', {'ads': ads})

    def post(self, request):
        ad_id = request.POST.get('ad_id')
        ad = get_object_or_404(Ad, id=ad_id)
        buyer = get_object_or_404(Profile, user=request.user)

        if ad.user == buyer.user:
            messages.error(request, 'You cannot start a chat with yourself.')
            return redirect('ads-list')

        seller = ad.user
        chat, created = Chat.objects.get_or_create(ad=ad, buyer=buyer, seller=seller)

        if created:
            messages.success(request, 'Chat created successfully!')
        else:
            messages.info(request, 'You already have an ongoing chat with this seller.')

        return redirect('ad_chat:chat_detail', chat_id=chat.id)
