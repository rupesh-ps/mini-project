from django.contrib import admin
from .models import Profile, Category, Ad, AdImages

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Ad)
admin.site.register(AdImages)