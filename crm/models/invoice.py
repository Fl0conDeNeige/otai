import random, string

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib import admin

from crm.constants import INVOICE_NUMBER_LENGTH
from .user import User

def _validate_new_number(new_number: str):
    if not _check_new_number(new_number=new_number):
        raise ValidationError("Already existing invoice number", params={'number': new_number})

def _check_new_number(new_number: str):
    if Invoice.objects.filter(invoice_number=new_number):
        return False
    return True

def _generate_new_invoice_number():
    new_number_lambda = lambda : f"OTA-{''.join(random.choice(string.digits) for i in range(INVOICE_NUMBER_LENGTH))}"
    new_number = new_number_lambda()
    while not _check_new_number(new_number=new_number):
        new_number = new_number_lambda()
    return new_number

class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT) # This also means that we can't delete users for which invoices exist. We could use SET_NULL if we want to enable it
    invoice_number = models.CharField(max_length=9, default=_generate_new_invoice_number, editable=False, blank=True, null=False, validators=[_validate_new_number])
    amount = models.FloatField(blank=False, null=False)
    date = models.DateTimeField("Invoiced date", auto_now_add=True, blank=True, null=False)
    paid = models.BooleanField(default=False, blank=True, null=False)

    def __str__(self):
        return self.invoice_number
