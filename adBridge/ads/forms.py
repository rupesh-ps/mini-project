from django import forms
from .models import Ad, AdImages, Category
from django.forms import inlineformset_factory
from django import forms
from .models import Ad, Profile
from django.forms import ValidationError
from django.utils import timezone
from datetime import datetime


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['category', 'title', 'description', 'tags', 'price', 'location', 'postal_code', 'contact_email', 'contact_phone', 'start_date', 'end_date', 'show_contact']

    def __init__(self, *args, **kwargs):
        super(AdForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['title'].widget.attrs.update({'placeholder': 'Enter the title of your ad'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Provide a detailed description of your ad'})

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        price = cleaned_data.get('price')
        contact_email = cleaned_data.get('contact_email')
        contact_phone = cleaned_data.get('contact_phone')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if isinstance(start_date, datetime):
            start_date = start_date.date() 
        if isinstance(end_date, datetime):
            end_date = end_date.date() 

        if category and category.type == 'sale' and price is None:
            raise ValidationError("Price is required for sale ads.")

        if category and category.type == 'job':
            if not contact_email or not contact_phone:
                raise ValidationError("Contact email and phone are required for job ads.")

        if category and category.name == 'Events':
            if not start_date or not end_date:
                raise ValidationError("Both start date and end date are required for events.")

            if start_date and end_date and start_date >= end_date:
                raise ValidationError("End date must be after the start date.")

            if start_date and start_date < timezone.now().date():
                raise ValidationError("Start date cannot be in the past.")
            if end_date and end_date < timezone.now().date():
                raise ValidationError("End date cannot be in the past.")
            
        return cleaned_data

class AdImageForm(forms.ModelForm):
    class Meta:
        model = AdImages
        fields = ('image', 'image_caption',)

AdImagesFormSet = inlineformset_factory(
    Ad,
    AdImages,
    form=AdImageForm,
    extra=1,
    can_delete=True  
)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'email']