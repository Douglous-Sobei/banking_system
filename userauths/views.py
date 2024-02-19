from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from userauths.models import User
from userauths.forms import UserRegistrationForm


def RegisterView(request):
    if request.user.is_authenticated:
        messages.warning(request, f"You are already logged in.")
        return redirect("core:index")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = new_user.username
            messages.success(
                request, f"Hey {username}, your account was created successfully")
            return redirect('core:index')
    else:
        form = UserRegistrationForm()

    context = {
        "form": form
    }
    return render(request, "userauths/sign-up.html", context)


def logoutView(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("core:index")


def LoginView(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in")
                return redirect("core:index")
            else:
                messages.warning(
                    request, "Username or password does not exist")
                return redirect("userauths:sign-in")
        except:
            messages.warning(request, "User does not exist")

    return render(request, "userauths/sign-in.html")
