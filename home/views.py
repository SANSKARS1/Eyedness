from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request , 'main.html')

@login_required(login_url='login')
def incident(request):
    return render(request , 'testing.html')