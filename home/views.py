from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
@login_required(login_url='/login')
def index(request):
    detail = userDetail.objects.filter(credential=request.user)
    param = {'detail':detail}
    return render(request, 'index.html', param)

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

def logout(request):
    auth.logout(request)
    messages.info(request, 'Thank You, Come Again')
    return redirect('/login')

def addTransactions(request):
    if request.method == 'POST':
        name = request.POST['name']
        amount = request.POST['amount']
        transtype = request.POST['type']
        user = userDetail.objects.filter(credential=request.user)
        trans = transaction(transaction_name=name, transaction_amount=amount, transaction_type=transtype, credential=request.user)
        if int(transtype) == 0:
            user_balance = user[0].current_balance
            updated_balance = user_balance + int(amount)
            user.update(current_balance=updated_balance)
        elif int(transtype) == 1:
            user_balance = user[0].current_balance
            updated_balance = user_balance - int(amount)
            user.update(current_balance=updated_balance)
        trans.save()                
        messages.info(request, 'Transaction Added')
        return redirect('/')

@login_required(login_url='/login')
def showTransaction(request):
    try:
        transactionData = transaction.objects.filter(credential=request.user)
        print(transactionData[0].transaction_type)
        userData = userDetail.objects.filter(credential=request.user)

        param = {'transactions':transactionData, 'user':userData}
        return render(request, 'transaction.html', param)
    except:
        messages.info(request, 'No Transaction Detected')
        return render('/')

@login_required(login_url='/login')
def account(request):
    detail = userDetail.objects.filter(credential=request.user)
    param = {'detail':detail}
    return render(request, 'account.html', param)

def updateAccount(request):
    if request.method == 'POST':
        income = request.POST['income']        
        balance = request.POST['balance']
        user = userDetail.objects.filter(credential=request.user)
        user.update(income=income, current_balance=balance)

        messages.success(request, 'Account Updated Successfully')
        return redirect('/account')

    else:
        return redirect('/')

def about(request):
    return render(request, 'about.html')        