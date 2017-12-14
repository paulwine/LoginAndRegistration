# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from models import *
from django.contrib import messages
import re

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

def index(request):
    

    request.session["init"] = True
    return render(request, 'index.html')

def new_user(request):
    print request.method
    error = False
    if request.method == "POST":
        first = request.POST["first_name"]
        last = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm = request.POST["confirm"]
        error = False
        if len(email) < 0 or len(password) < 0 or len(first) < 0 or len(last) < 0:
            messages.add_message(request, messages.INFO, "Please Input All Fields")
            error = True
        if len(password) < 8:
            messages.add_message(request, messages.INFO, "Passwords must be longer than 8 characters")
            error = True
        if password != confirm:
            messages.add_message(request, messages.INFO, "Passwords must match")
            error = True
        if not re.match(EMAIL_REGEX, email):
            messages.add_message(request, messages.INFO, "Email must be in proper format")
            error = True

        if error == True:
            print "There was an error numnuts"
            return redirect("/new_user")

        request.session["context"] = {
            "first" : first,
            "last" : last,
            "email" : email,
            "password" : password,
            "confirm" : confirm
        }
        User.objects.create(first_name=first,last_name=last, email=email, password=password)
        
        return redirect("/main")
    else:
        return redirect("/")
def login(request):
    print request.method
    error = False
    if request.method == "POST":
        error = False
        email = request.POST["email"]
        password = request.POST["password"]
        first = User.objects.filter(email=email)
        if len(email) < 0 or len(password) < 0:
            messages.add_message(request, messages.INFO, "Please Input All Fields")
            error = True
        current_user = User.objects.filter(email=email)

        if len(current_user) < 1:
            messages.add_message(request, messages.INFO, "No users in database")
            error = True
        for user in current_user:
            if user.email != email or user.password != password:
                messages.add_message(request, messages.INFO, "Email or password did not match user in database.")
                error = True

        if error == True:
            return redirect("/")    

        
        request.session["context"] = {
            "first" : first[0].first_name,
            "email" : email,
            "password" : password
           
        }
        print "hey"
        return redirect("/main")

def main(request):
    context = request.session["context"]
    all_users = User.objects.all()
    context["all_users"] = all_users
    print all_users
    all
    return render(request, "main.html", context)

def dump_users(request):
    User.objects.all().delete()
    return redirect("/main")

def logout(request):
    if request.session:
        for key in request.session.keys():
            del request.session[key]
    return redirect("/")
# Create your views here.
