from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    if request.user.is_anonymous:
        if request.method == 'POST':
            username = request.POST['number']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Welcome!')
                return redirect('/')

            else:
                messages.warning(request, 'Invailid Username or Password')
                return redirect('/login') 

        else:
            return render(request, 'login.html')    
            
    else:
        messages.info(request, 'Already Login')
        return redirect('/')  

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        number = request.POST['number']
        email = request.POST['email']
        income = request.POST['income']
        password = request.POST['password']

        if User.objects.filter(username=number).exists() and User.objects.filter(email=email).exists():
            messages.warning(request, 'Already Registered')
            return redirect('/signup')

        else:    
            user = User.objects.create_user(username = number, password = password, email = email, first_name = name)
            user.save()
            detail = userDetail(income=income, credential=user, current_balance=income)
            detail.save()
            messages.info(request, 'Account Created Successfully')
            return redirect('/login')

    else:
        return render(request, 'signup.html')    