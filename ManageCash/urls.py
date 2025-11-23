from django.urls import path
from .views import (
    dashboard_view,
    register_view,
    login_view,
    logout_view,
    profile_view,
    profile_update_view,
    cash_list_view,
    add_cash_view,
    edit_cash_view,
    delete_cash_view,
    expense_list_view,
    add_expense_view,
    edit_expense_view,
    delete_expense_view,
)

urlpatterns = [
    # Dashbaord===================
    path("", dashboard_view, name="dashboard"),
    # Authentication==============
    path("auth/register/", register_view, name="register"),
    path("auth/login/", login_view, name="login"),
    path("auth/logout/", logout_view, name="logout"),
    # Profile ==============
    path("profile/", profile_view, name="profile"),
    path("profile/update/", profile_update_view, name="profile_update"),
    # Cash CRUD =============
    path("cash/list/", cash_list_view, name="cash_list"),
    path("cash/add/", add_cash_view, name="add_cash"),
    path("cash/edit/", edit_cash_view, name="edit_cash"),
    path("cash/del/", delete_cash_view, name="delete_cash"),
    # Expense CRUD =============
    path("expense/list/", expense_list_view, name="expense_list"),
    path("expense/add/", add_expense_view, name="add_expense"),
    path("expense/edit/", edit_expense_view, name="edit_expense"),
    path("expense/del/", delete_expense_view, name="delete_expense"),
]
