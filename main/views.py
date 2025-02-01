from django.shortcuts import render,HttpResponse

def index(request):
    return render(request,'index.html')

def dashboard(request):
    return render(request,'dashboard.html')

def step(request):
    return render(request,'steps.html')


