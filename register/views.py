from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout,user_logged_out
from django.contrib.auth.forms import UserCreationForm
from .forms import RegsiterForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
# Create your views here.
def register(response):
    if response.method == 'POST':
        form = RegsiterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = RegsiterForm()
    return render(response, 'register/register.html',{"form":form})


def user_logout(request):
    logout(request)
    return redirect('/login/')


def send_mail_user(request):
    username=request.GET['username']
    password=request.GET['password']
    email=User.objects.get(username=username).email
    subject='Your account information'
    message="Username:"+username+"\n"+"Password:"+password
    #send mail to the user with his/her account info
    from_email='admin@gmail.com'
    to=[email]
    send_mail(subject,message,from_email,to,fail_silently=False)
    return redirect("/")  

