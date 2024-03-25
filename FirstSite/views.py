#our file
from django.http import HttpResponse
from django.shortcuts import render
def index(requests):
    return render(requests,"index.html")
    # return HttpResponse('''<h1>Hello</h1> <a href="https://www.instagram.com/hussain.mohammedmushtaq"> MyInstaHandle</a> <br>
    #                     <a href ="https://www.codechef.com/users/kanieloutis13"> CodeChef Profile</a> <br>
    #                     <a href='about'>About</a>''') 
def about(requests):
    return HttpResponse("Hello About <br> <a href='/'>Back</a>") 