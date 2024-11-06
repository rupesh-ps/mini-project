from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect

from .forms import SignUpForm

def signup(request):
    
    if request.user.is_authenticated:
        return redirect('homepage')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})
