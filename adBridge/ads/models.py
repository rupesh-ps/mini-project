from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

CATEGORY_CHOICES = [
    ('job', 'Job'),
    ('gig', 'Gig'),
    ('rental', 'Rental'),
    ('sale', 'Sale'),
    ('service', 'Service'),
    ('event', 'Event'),
    ('class', 'Class'),
    ('other', 'Other'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    phone = models.CharField(_('Contact phone'), max_length=15)
    email = models.EmailField(_("Email"), max_length=25)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(_("Category Name"), max_length=50)
    type = models.CharField(_("Category Type"), max_length=50, choices=CATEGORY_CHOICES)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
class Ad(models.Model):
    user = models.ForeignKey(Profile, related_name="poster", verbose_name=_("User"), on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='category', verbose_name=_("Category"), on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=50)
    tags = TaggableManager() 
    location = models.TextField(_("Location"))
    postal_code = models.IntegerField(_("Postal Code"))
    description = models.TextField(_("Description"))
    show_contact = models.BooleanField(_("Show Contact"), default=False)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2, null=True, blank=True)
    contact_email = models.EmailField(_("Contact Email"), null=True, blank=True)
    contact_phone = models.CharField(_("Contact Phone"), max_length=25, null=True, blank=True)
    posted_at = models.DateTimeField(_("Posted On"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated On"), auto_now=True)
    view = models.PositiveIntegerField(_("Total Views"), default=0)
    start_date = models.DateTimeField(_("Start Date"), null=True, blank=True)
    end_date = models.DateTimeField(_("End Date"), null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.category.type == 'sale' and self.price is None:
            raise ValueError(_("Price is required for sale ads."))
        if self.category.type == 'job' and (self.contact_email is None or self.contact_phone is None):
            raise ValueError(_("Contact email and phone are required for job ads."))
        super().save(*args, **kwargs)
          
    def __str__(self):
        return f"{self.title} ({self.category.name})"

class AdImages(models.Model):
    ad = models.ForeignKey(Ad, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(_("Image"), upload_to="ads/images/")
    image_caption = models.CharField(_("Caption"), max_length=100, blank=True)

    def __str__(self):
        return f"Image for {self.ad.title} with caption: {self.image_caption}"

class Message(models.Model):
    ad = models.ForeignKey(Ad, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField(_("Message"))
    user = models.ForeignKey(Profile, related_name='messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    def __str__(self):
        return f"Message from {self.user.user.username} regarding {self.ad.title}"
