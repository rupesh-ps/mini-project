from django.urls import path
from . import views

app_name = 'ad_chat'
urlpatterns = [
    path('create_chat/<int:ad_id>/', views.create_chat, name='create_chat'),
    path('<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('new/', views.new_message, name='new_message'),
    path('inbox/', views.inbox, name='seller_inbox'),
]
