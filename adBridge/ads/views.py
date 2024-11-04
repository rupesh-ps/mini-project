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
        if search_query:
            queryset = queryset.filter(
                    title__icontains=search_query
            ).union(
                queryset.filter(description__icontains=search_query)
            )
        return queryset

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

