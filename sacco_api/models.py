from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from decimal import Decimal

class Member(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    account_balance = models.DecimalField(max_digits=10, decimal_places=2)
    membership_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.full_name


class Savings(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2)
    membership_number = models.CharField(max_length=20)

    def __str__(self):
        return f"Savings Account #{self.id} for {self.member.full_name}"

    def withdraw(self, amount):
        """
        Method to withdraw from savings.
        Deducts the specified amount from the account balance.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be a positive value")

        if self.account_balance < amount:
            raise ValueError("Insufficient savings balance")

        new_balance = self.account_balance - Decimal(amount)
        self.account_balance = new_balance
        self.save()
        return new_balance
