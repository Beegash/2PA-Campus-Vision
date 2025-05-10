from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # Ana sayfaya yönlendir
        else:
            return render(request, 'login_c.html', {'error': 'Invalid username or password'})
    return render(request, 'login_c.html')
