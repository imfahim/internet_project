from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.hghghg

def home(request):
    return render(request, "internetProject/signup.html")

def signup(request):
    return render(request, "internetProject/signup.html")

def signin(request):
    return render(request, "internetProject/signin.html")

def signout(request):
   pass


