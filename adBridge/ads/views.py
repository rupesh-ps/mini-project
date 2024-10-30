from django.views.generic import TemplateView, ListView, DetailView
from .models import Category, Ad

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
    paginate_by =10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ads'] = Ad.objects.filter(category=self.object.id)
        return context

class AdListView(ListView):
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    paginate_by = 10

class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'
