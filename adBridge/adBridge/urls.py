from django.contrib import admin
from django.urls import path
from ads import views
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePageView.as_view(), name='homepage'),
    path("signup/", accounts_views.signup, name="signup"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("login/", auth_views.LoginView.as_view(template_name='accounts/login.html',redirect_authenticated_user=True), name="login"),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path("ads/", views.AdListView.as_view(), name="ad-list"),
    path('ad/create/', views.AdCreateView.as_view(), name='ad-create'),
    path('ad/<int:pk>/', views.AdDetailView.as_view(), name='ad-detail'),
    path('ad/<int:pk>/edit/', views.AdUpdateView.as_view(), name='ad-update'),
    path('ad/<int:pk>/delete/', views.AdDeleteView.as_view(), name='ad-delete'),
    path('featured', views.FeaturedView.as_view(), name="featured-ads"),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile-edit'),
    path('reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt'
    ), name='reset_password'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('settings/password/', login_required(auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change.html')),
        name='password_change'),
    path('settings/password/done/', login_required(auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html')),
        name='password_change_done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)