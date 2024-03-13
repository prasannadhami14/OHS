from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse 
from OnlineHotelReservation import settings
from django.core.mail import send_mail,EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text
from .tokens import generate_token

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request,'hotel/index.html')
def register_user(request):
     if request.method=='POST':
        username=request.POST["username"]
        email=request.POST["email"]
        firstName=request.POST["fname"]
        LastName=request.POST["lname"]
        password=request.POST["password"]
        cpassword=request.POST["cpassword"]
        if len(firstName)<3:
            message = "Firstname must be at least 3 characters"
            return redirect(reverse('users:register') + '?message=' + message) 
        if len(username)<3:
            message = "username must be at least 4 characters"
            return redirect(reverse('users:register') + '?message=' + message) 
        if len(LastName)<2:
            message = "lastname must be at least 3 characters"
            return redirect(reverse('users:register') + '?message=' + message) 
        if len(password) < 8:
              message = "Password must be at least 8 characters long"
              return redirect(reverse('users:register') + '?message=' + message) 

        if not any(c.isupper() for c in password):
              message = "Password must contain at least one uppercase lette"
              return redirect(reverse('users:register') + '?message=' + message) 

        if not any(c.islower() for c in password):
              message = "Password must contain at least one lowercase letter"
              return redirect(reverse('users:register') + '?message=' + message) 

             
        if not any(c.isdigit() for c in password):
               message = "Password must contain at least one digit"
               return redirect(reverse('users:register') + '?message=' + message) 

        if not any(c in "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~" for c in password):
            message = "Password must contain at least one special character"
            return redirect(reverse('users:register') + '?message=' + message)

        if User.objects.filter(username=username):
            message = "Username already exists"
            return redirect(reverse('users:register') + '?message=' + message)


        if User.objects.filter(email=email):
            message = "email already exists"
            return redirect(reverse('users:register') + '?message=' + message)
        if password!= cpassword:
            message = "confirm password didnt match"
            return redirect(reverse('users:register') + '?message=' + message)
        else:
            myuser=User.objects.create_user(username,email,password)
            myuser.first_name=firstName
            myuser.last_name=LastName
            myuser.is_active=False
            myuser.save()
            messages="Successfully registered your account"
            # email for registration
            subject="Welcome message!!!"
            message=" Hello " + myuser.first_name+" \nwelcome to  Hotel APPS! \n please check  another email with activation link to activate your account.\n Thank you for visting us."
            from_email=settings.EMAIL_HOST_USER
            to_list=[myuser.email]
            send_mail(subject,message,from_email,to_list,fail_silently=True)    
            # FOR account activation
            current_site=get_current_site(request)
            email_subject="Activate your account"
            message2=render_to_string('email_confirmation.html',{
                'name': myuser.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser),
            })
            email=EmailMessage(
                               email_subject,
                               message2,
                               settings.EMAIL_HOST_USER,
                               [myuser.email]
            )
            email.fail_silently=True
            email.send()     
            message="Check you email to activate you account"    
            return redirect(reverse('users:login')+ '?message=' + message)
     return render(request,'customer/registerUser.html',{'messages': messages})

def activate(request,uidb64,token):
    try:
        uid=force_text(urlsafe_base64_decode(uidb64))
        myuser=User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser=None
    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active=True
        myuser.save()
        login(request,myuser)
        return redirect('hotels:index')
    else:
        return render(request,'activation_failed.html')
def login_user(request):
    if request.method=='POST':
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            message = "Login Sucessfully"
            return redirect(reverse('hotels:index') + '?message=' + message)
        else:
            message = "Invalid credentials"
            return redirect(reverse('users:login') + '?message=' + message)
        
    else:
        return render(request,'customer/login.html')
def logout_user(request):
    logout(request)
    message = "Logout Sucessfully"
    return redirect(reverse('hotels:index') + '?message=' + message)
def loginForm(request):
    return render(request,'customer/login.html')
def registerForm(request):
    return render(request,'customer/registerUser.html')