from django.contrib import admin
from django.urls import path
from ads import views
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePageView.as_view(), name='homepage'),
    path("signup/", accounts_views.signup, name="signup"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("login/", auth_views.LoginView.as_view(template_name='accounts/login.html'), name="login"),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path("ads/", views.AdListView.as_view(), name="ad-list"),
    path('ad/<int:pk>/', views.AdDetailView.as_view(), name='ad-detail'),
    path('featured', views.FeaturedView.as_view(), name="featured-ads"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)