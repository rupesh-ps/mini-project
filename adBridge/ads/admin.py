from django.contrib import admin
from .models import Profile, Category, Ad, Message

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Ad)
admin.site.register(Message)