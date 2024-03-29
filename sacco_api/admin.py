from django.contrib import admin
from .models import Member, Savings

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number', 'date_of_birth', 'account_balance', 'membership_number']
    search_fields = ['full_name', 'phone_number', 'membership_number']
    list_filter = ['date_of_birth']
    readonly_fields = ['account_balance']

@admin.register(Savings)
class SavingsAdmin(admin.ModelAdmin):
    list_display = ['id', 'member', 'account_balance', 'membership_number']
    search_fields = ['member__full_name', 'membership_number']
    list_filter = ['member__full_name']
