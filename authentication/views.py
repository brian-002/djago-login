from django.http import HttpResponse
from django.shortcuts import redirect, render
from . import views
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from gfg import settings
from django.core.mail import send_mass_mail, send_mail

# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username = username, password = pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname': fname}) 
        
        else:
            messages.error(request, "credentials dont match")
            return redirect('home')


    return render(request, "authentication/signin.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username = username):
            messages.error(request, "user already exists")
            return redirect('home')

        if User.objects.filter(email = email):
            messages.error(request, "email already exists")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "passwords donot match")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "username must be alphanumeric")
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "your account as been successfuly created")


        subject = "welcome to django login practice page"
        message = "hello" + myuser.first_name + myuser.last_name + " \n " + "welcome to djago login \n" + "thankyou for registering with us\n we have sent you a confirmation email"
        from_email= settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect('signin')


    return render(request, "authentication/signup.html")

def signout(request):
    logout(request)
    messages.success(request, "logged out successfuly")
    
    return redirect('home')