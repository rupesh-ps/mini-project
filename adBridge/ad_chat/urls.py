from django.urls import path
from .views import CreateChatView, ChatDetailView, NewMessageView, InboxView

app_name = 'ad_chat'
urlpatterns = [
    path('create_chat/<int:ad_id>/', CreateChatView.as_view(), name='create_chat'),
    path('<int:chat_id>/', ChatDetailView.as_view(), name='chat_detail'),
    path('new/', NewMessageView.as_view(), name='new_message'),
    path('inbox/', InboxView.as_view(), name='seller_inbox'),
]
