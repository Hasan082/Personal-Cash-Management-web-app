from django.contrib import admin
from .models import Profile, AddCash, Expense

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'age')

@admin.register(AddCash)
class AddCashAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'source', 'amount', 'description')

@admin.register(Expense)
class ExpenceAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'amount', 'description')
