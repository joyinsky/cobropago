from django.contrib import admin
from .models import *


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ledger', 'date', 'account', 'payee', 'amount')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ledger', 'name', 'balance')


@admin.register(Payee)
class PayeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ledger', 'name')


@admin.register(Ledger)
class LedgerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name')