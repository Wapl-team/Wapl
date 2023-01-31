from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http.request import HttpRequest


# Create your views here.

def main(request:HttpRequest, *args, **kwargs):
    return render(request, "main.html")

def login(request:HttpRequest, *args, **kwargs):
    return render(request, "login.html")