from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from .models import Chat, ChatMessage
from ads.models import Ad, Profile

def is_user_in_chat(chat, user):
    return chat.buyer.user == user or chat.seller.user == user

@login_required
def create_chat(request, ad_id):
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

@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if not is_user_in_chat(chat, request.user):
        messages.error(request, 'You are not authorized to view this chat.')
        return redirect('home')
    
    messages_in_chat = ChatMessage.objects.filter(chat=chat).order_by('created_at')

    for message in messages_in_chat:
        message.can_edit = message.sender.user == request.user and (timezone.now() - message.created_at <= timedelta(minutes=2))
        message.can_delete = message.sender.user == request.user

    if request.method == 'POST':
        message_text = request.POST.get('message')
        message_id = request.POST.get('message_id')

        if message_text:
            if message_id:
                message = get_object_or_404(ChatMessage, id=message_id)
                if message.sender.user == request.user and timezone.now() - message.created_at <= timedelta(minutes=2):
                    message.message = message_text
                    message.updated_at = timezone.now()
                    message.save()
                    messages.success(request, 'Message updated successfully.')
                else:
                    messages.error(request, 'You can only edit your messages within 2 minutes of sending.')
            else:
                sender = chat.buyer if chat.buyer.user == request.user else chat.seller
                ChatMessage.objects.create(chat=chat, sender=sender, message=message_text)
                messages.success(request, 'Message sent successfully.')

            return redirect('ad_chat:chat_detail', chat_id=chat.id)

        elif 'delete_message' in request.POST:
            message_id = request.POST.get('delete_message')
            message = get_object_or_404(ChatMessage, id=message_id)

            if message.sender.user == request.user:
                message.delete()
                messages.success(request, 'Message deleted successfully.')
            else:
                messages.error(request, 'You can only delete your own messages.')

            return redirect('ad_chat:chat_detail', chat_id=chat.id)

    return render(request, 'ad_chat/chat.html', {
        'chat': chat,
        'messages': messages_in_chat,
    })

@login_required
def inbox(request):
    profile = get_object_or_404(Profile, user=request.user)
    chats = Chat.objects.filter(seller=profile).order_by('-created_at')

    return render(request, 'ad_chat/inbox.html', {
        'chats': chats,
    })
