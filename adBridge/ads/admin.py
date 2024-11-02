from django.contrib import admin
from .models import Profile, Category, Ad, Message, AdImages

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Ad)
admin.site.register(Message)
admin.site.register(AdImages)