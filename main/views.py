from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login , logout
#from .middlewares import auth,guest

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('dashboard')
    else:
        initial_data = {'username' : '' , 'password1' :'' , 'password2':''}
        form = UserCreationForm(initial= initial_data)
    return render(request, 'auth/register.html' , {'form' : form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('dashboard')
    else:
        initial_data = {'username' : '' , 'password' :''}
        form = AuthenticationForm(initial= initial_data)
    return render(request, 'auth/login.html' , {'form' : form})  

def logout_view(request):
    logout(request)
    return redirect('index')

def index(request):
    return render(request,'index.html')

def dashboard(request):
    return render(request,'dashboard.html')

def step(request):
    return render(request,'steps.html')


