from decimal import Decimal
import uuid

from django.db import models


class Loan(models.Model):
    identifier = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    nominal_value = models.DecimalField(max_digits=15, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=6, decimal_places=5)
    ip_address = models.GenericIPAddressField(default='0.0.0.0')
    request_date = models.DateField(auto_now_add=True)
    bank = models.CharField(max_length=100)
    client = models.CharField(max_length=100)
    iof_rate = models.DecimalField(
        max_digits=6, decimal_places=5, default=Decimal('0.00'))
    insurance_rate = models.DecimalField(
        max_digits=6, decimal_places=5, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


class Payment(models.Model):
    loan = models.ForeignKey(
        Loan, related_name='payments', on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
