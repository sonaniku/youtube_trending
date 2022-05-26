from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
# Create your views here.
@login_required(login_url='/login/')
def home(request):
    
    context = {}
    return render(request, 'home/index.html', context=context)

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login:login")