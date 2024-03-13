from django.shortcuts import redirect, render


from django.contrib.auth.models import User
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        
        return redirect('rooms:index') 
    else:
        return redirect('customers:register')

