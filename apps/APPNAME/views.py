# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User

# Create your views here.
def index(request):
    request.session['errors']=[]
    context={
    "users":User.objects.all()
    }
    return render(request, 'APPNAME/index.html', context)

def register(request):
    request.session['errors'] = []
    for user in User.objects.all():
        if request.POST['reg_email']==user.email:
            request.session['errors'].append("Entered email already exists!")
#↓↓↓↓↓checking email validity↓↓↓↓↓
    dotcounter=0
    atcounter=0
    for i in request.POST['reg_email']:
        if i.find(".")!=-1:
            dotcounter=dotcounter+1
        if i.find("@")!=-1:
            atcounter=atcounter+1
    if dotcounter>0 and atcounter>0:
        email_validity=True
    else: email_validity=False
#↑↑↑↑↑chedking email validity↑↑↑↑↑

    if email_validity==False:
        request.session['errors'].append("Please enter valid email address.")
    if len(request.POST['reg_first_name'])<2:
        request.session['errors'].append("First name length must be greater than 2 characters.")
    if len(request.POST['reg_last_name'])<2:
        request.session['errors'].append("Last name length must be greater than 2 characters.")
    if len(request.POST['reg_password'])<8:
        request.session['errors'].append("Password must be 8 characters of longer")
    if request.POST['reg_password']!=request.POST['reg_password_confirm']:
        request.session['errors'].append("Password and Confirm pw are different.")

    if len(request.POST['reg_first_name'])<2 or len(request.POST['reg_last_name'])<2 or request.POST['reg_email']=="" or len(request.POST['reg_password'])<8 or request.POST['reg_password']!=request.POST['reg_password_confirm']:
        return render(request, 'APPNAME/index.html')
    else:
        User.objects.create(first_name=request.POST['reg_first_name'], last_name=request.POST['reg_last_name'], email=request.POST['reg_email'], password=request.POST['reg_password'])
        return redirect('/')

def login(request):
    request.session['errors'] = []
    for user in User.objects.all():
        if request.POST['log_email']==user.email and request.POST['log_password']==user.password:
            request.session['first_name']=user.first_name
            return redirect('/success')
        else:
            continue
    request.session['errors'].append("Either username or password is incorrect.")
    return render(request, 'APPNAME/index.html')
def success(request):
    return render(request, 'APPNAME/success.html')
