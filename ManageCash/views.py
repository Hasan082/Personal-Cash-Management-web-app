from django.shortcuts import render, redirect
from .models import Profile, AddCash, Expense
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib import messages

# AUTH VIEWS==============================


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()
    context = {"form": form}
    return render(request, "auth/register.html", context)


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid Credintetials!")
            return redirect("login")
    else:
        form = AuthenticationForm()

    context = {"form": form, "login_form": True}

    return render(request, "auth/login.html", context)

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


# DASHBOARD VIEWS==============================


@login_required
def dashboard_view(request):

    return render(request, "pages/dashboard.html")


# PROFILE VIEWS==============================


@login_required
def profile_view(request):

    return render(request, "pages/profile.html")


# CASH VIEWS==============================


@login_required
def cash_list_view(request):

    return render(request, "pages/cash-list.html")


@login_required
def add_cash_view(request):

    return render(request, "pages/cash.html")


@login_required
def edit_cash_view(request):

    return render(request, "pages/cash.html")


@login_required
def delete_cash_view(request):

    return render(request, "pages/cash.html")


# EXPENSE VIEWS==============================


@login_required
def expense_list_view(request):

    return render(request, "pages/expense-list.html")


@login_required
def add_expense_view(request):

    return render(request, "pages/expense.html")


@login_required
def edit_expense_view(request):

    return render(request, "pages/expense.html")


@login_required
def delete_expense_view(request):

    return render(request, "pages/cash.html")
