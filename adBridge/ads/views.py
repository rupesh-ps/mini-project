from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Category, Ad, Profile
from .forms import AdForm, AdImagesFormSet, ProfileForm, ContactForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from taggit.models import Tag

class HomePageView(TemplateView):
    template_name = 'base.html'

class CategoryListView(ListView):
    model = Category
    template_name = 'ads/category_list.html'
    context_object_name = 'categories'
    paginate_by = 10
    ordering = ['id']

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'ads/category_detail.html'
    context_object_name = 'category'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ads'] = Ad.objects.filter(category=self.object.id)
        return context

class AdListView(ListView):
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        tags = self.request.GET.get('tags')

        if search_query:
            queryset = queryset.filter(
                    title__icontains=search_query
            ).union(
                queryset.filter(description__icontains=search_query)
            )

        if tags:
            tag_list = tags.split(",")
            queryset = queryset.filter(tags__name__in=tag_list).distinct()

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context

class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'

    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        ad.view += 1
        ad.save(update_fields=['view'])

        return super().get(request, *args, **kwargs)

class FeaturedView(ListView):
    model = Ad
    template_name = 'ads/featured_ads.html'
    context_object_name = 'featured_ads'
    paginate_by = 10

    def get_queryset(self):
        return Ad.objects.all().filter(view__gte=3).order_by('-view')[:10]

class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_create.html'

    def get_success_url(self):
        return reverse_lazy('ad-detail', args=[self.object.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = AdImagesFormSet()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user.profile
        image_form = AdImagesFormSet(self.request.POST, self.request.FILES, instance=self.object)

        if form.is_valid() and image_form.is_valid():
            self.object = form.save()
            image_form.instance = self.object
            image_form.save()
            return HttpResponseRedirect(self.get_success_url())

        return self.form_invalid(form)
    
class AdUpdateView(LoginRequiredMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_update.html'

    def get_object(self):
        ad = get_object_or_404(Ad, pk=self.kwargs['pk'], user=self.request.user.profile)
        return ad
     
    def get_success_url(self):
        return reverse_lazy('ad-detail', args=[self.object.id])

    def get_context_data(self, **kwargs):
            context = super(AdUpdateView, self).get_context_data(**kwargs)
            if self.request.POST:
                context['image_form'] = AdImagesFormSet(self.request.POST,self.request.FILES, instance=self.object)
            else:
                context['image_form'] = AdImagesFormSet(instance=self.object)
            return context
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user.profile)

    def form_valid(self, form):
        context = self.get_context_data()
        image_form = context['image_form']
        form.save()

        if form.is_valid() and image_form.is_valid():
            self.object = form.save()
            image_form.instance =  self.object
            image_form.save()
            return HttpResponseRedirect(self.get_success_url())

        return self.form_invalid(form)
    
class AdDeleteView(LoginRequiredMixin, DeleteView):
    model = Ad
    template_name = 'ads/ad_delete.html'
    context_object_name = 'ad'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user.profile)
    
    def get_success_url(self):
        return reverse_lazy('ad-list') 

class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_ads = Ad.objects.filter(user=self.get_object())
        context['user_ads'] = user_ads
        return context
    
class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile_update.html'
    success_url = '/profile/'
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    
def support(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            send_mail(
                f"User {name} messaged via Contact Form",
                message,
                email,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            
            return redirect('contact_success') 
        
    else:
        form = ContactForm()
    
    return render(request, 'site/support.html', {'form': form})

def contact_success(request):
    return render(request, 'site/contact_success.html')

def custom_404(request, exception):
    return render(request, '404.html', status=404)