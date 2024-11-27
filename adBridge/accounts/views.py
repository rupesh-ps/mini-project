from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect

from .forms import SignUpForm
from ads.models import Profile

def signup(request):
    
    if request.user.is_authenticated:
        return redirect('homepage')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user, email=user.email, phone="")
            auth_login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})
