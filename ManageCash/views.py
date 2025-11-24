from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, AddCash, Expense
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, ProfileForm, AddCashForm, ExpenseForm
from django.contrib import messages
from django.db.models import Sum
import json
from django.utils import timezone
from datetime import datetime

# AUTH VIEWS==============================


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successfull! Please login now!")
            return redirect("login")
        else:
            messages.error(request, "Please check all info and try again!")
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
            messages.success(request, "Login successful!")
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
    messages.success(request, "System Logout successfully!")
    return redirect("login")


# DASHBOARD VIEWS==============================


@login_required
def dashboard_view(request):
    cash_qs = AddCash.objects.filter(user=request.user)
    exp_qs = Expense.objects.filter(user=request.user)

    cash_in = cash_qs.aggregate(total=Sum("amount"))["total"] or 0
    exp_total = exp_qs.aggregate(total=Sum("amount"))["total"] or 0
    balance = cash_in - exp_total

    # Recent transactions (merge incomes and expenses by datetime)
    incomes = list(cash_qs.order_by("-datetime")[:8])
    expenses = list(exp_qs.order_by("-datetime")[:8])
    recent_tx = sorted(incomes + expenses, key=lambda o: o.datetime or timezone.now(), reverse=True)[:8]

    # Monthly totals for last 6 months
    now = timezone.now()
    start_of_current = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_labels = []
    monthly_income = []
    monthly_expense = []
    for i in range(5, -1, -1):
        year = start_of_current.year
        month = start_of_current.month - i
        while month <= 0:
            month += 12
            year -= 1
        start = datetime(year, month, 1, 0, 0, 0, tzinfo=timezone.get_current_timezone())
        if month == 12:
            end = datetime(year + 1, 1, 1, 0, 0, 0, tzinfo=timezone.get_current_timezone())
        else:
            end = datetime(year, month + 1, 1, 0, 0, 0, tzinfo=timezone.get_current_timezone())

        label = start.strftime("%b %Y")
        monthly_labels.append(label)

        inc = AddCash.objects.filter(user=request.user, datetime__gte=start, datetime__lt=end).aggregate(total=Sum("amount"))["total"] or 0
        exp = Expense.objects.filter(user=request.user, datetime__gte=start, datetime__lt=end).aggregate(total=Sum("amount"))["total"] or 0
        monthly_income.append(float(inc))
        monthly_expense.append(float(exp))

    # Top expenses for small chart
    top_expenses = list(Expense.objects.filter(user=request.user).order_by("-amount")[:5])
    top_exp_labels = [ (e.description[:30] if e.description else (e.datetime.strftime('%Y-%m-%d') if e.datetime else str(e.amount))) for e in top_expenses ]
    top_exp_values = [ float(e.amount) for e in top_expenses ]
    # average monthly spend (last 3 months)
    last3 = monthly_expense[-3:]
    avg_monthly_spend = round(sum(last3) / len(last3), 2) if last3 and len(last3) > 0 else 0
    # average monthly income (last 3 months)
    last3_inc = monthly_income[-3:]
    avg_monthly_income = round(sum(last3_inc) / len(last3_inc), 2) if last3_inc and len(last3_inc) > 0 else 0

    context = {
        "cash_in": cash_in,
        "exp_data": exp_total,
        "balance": balance,
        "recent_tx": recent_tx,
        "avg_monthly_spend": avg_monthly_spend,
        "avg_monthly_income": avg_monthly_income,
        "monthly_labels_json": json.dumps(monthly_labels),
        "monthly_income_json": json.dumps(monthly_income),
        "monthly_expense_json": json.dumps(monthly_expense),
        "top_exp_labels_json": json.dumps(top_exp_labels),
        "top_exp_values_json": json.dumps(top_exp_values),
    }
    return render(request, "pages/dashboard.html", context)


# PROFILE VIEWS==============================
def profile_view(request):
    return render(request, "pages/profile.html")


@login_required
def profile_update_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile info updated successfully!")
            return redirect("profile")
        else:
            messages.error(request, "Please check the info amd try again!")
    else:
        form = ProfileForm(instance=profile)

    context = {"form": form}

    return render(request, "pages/profile-update.html", context)


# CASH VIEWS==============================


@login_required
def cash_list_view(request):

    cash_data = AddCash.objects.all()
    context = {"cash_data": cash_data}

    return render(request, "pages/cash-list.html", context)


@login_required
def add_cash_view(request):
    if request.method == "POST":
        form = AddCashForm(request.POST)
        if form.is_valid():
            cash_user = form.save(commit=False)
            cash_user.user = request.user
            cash_user.save()
            messages.success(request, "Cash added successfully!")
            return redirect("cash_list")
        else:
            messages.error(request, "Cash add failed! Try Again!")
    else:
        form = AddCashForm()

    context = {"form": form}

    return render(request, "pages/cash.html", context)


def single_cash_view(request, id):

    return render(request, "pages/single-cash.html")


@login_required
def edit_cash_view(request, id):
    cash = get_object_or_404(AddCash, id=id, user=request.user)
    if request.method == "POST":
        form = AddCashForm(request.POST, instance=cash)
        if form.is_valid():
            form.save()
            messages.success(request, "Cash Updated successfully!")
            return redirect("cash_list")
        else:
            messages.error(request, "Please Try again!")
    else:
        form = AddCashForm(instance=cash)
    context = {"form": form, "edit": True}
    return render(request, "pages/cash.html", context)


@login_required
def delete_cash_view(request, id):
    if request.method == "POST":
        cash = get_object_or_404(AddCash, id=id, user=request.user)
        cash.delete()
        messages.success(request, "Cash record deleted successfully.")
        return redirect("cash_list")
    return redirect("cash_list")


# EXPENSE VIEWS==============================


@login_required
def expense_list_view(request):

    exp_data = Expense.objects.all()
    context = {"exp_data": exp_data}

    return render(request, "pages/expense-list.html", context)


@login_required
def add_expense_view(request):

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            exp_user = form.save(commit=False)
            exp_user.user = request.user
            exp_user.save()
            messages.success(request, "Expense added successfully!")
            return redirect("expense_list")
        else:
            messages.error(request, "Expense add failed! Try Again!")
    else:
        form = ExpenseForm()

    context = {"form": form}

    return render(request, "pages/expense.html", context)


@login_required
def edit_expense_view(request, id):
    exp = get_object_or_404(Expense, id=id, user=request.user)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=exp)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense Updated successfully!")
            return redirect("expense_list")
        else:
            messages.error(request, "Please Try again!")
    else:
        form = ExpenseForm(instance=exp)
    context = {"form": form, "edit": True}
    return render(request, "pages/expense.html", context)


@login_required
def delete_expense_view(request, id):
    if request.method == "POST":
        exp = get_object_or_404(Expense, id=id, user=request.user)
        exp.delete()
        messages.success(request, "Expense record deleted successfully.")
        return redirect("expense_list")
    return redirect("expense_list")
