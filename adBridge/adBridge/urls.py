from django.contrib import admin
from django.urls import path
from ads import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePageView.as_view(), name='homepage'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path("ads/", views.AdListView.as_view(), name="ad-list"),
    path('ad/<int:pk>/', views.AdDetailView.as_view(), name='ad-detail'),
]
