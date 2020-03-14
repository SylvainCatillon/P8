from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

from .forms import CustomUserCreationForm


def create(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("accounts:my_account")
            #else:
            #     return error message
        # else:
        #     print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/create.html", {"form": form})

def my_account(request):
    if request.user.is_authenticated:
        return render(request, "accounts/my_account.html")
    return redirect("accounts:login")
