import datetime

from django.db import models
from django.db.models import Sum
from django.utils import timezone


class User(models.Model):
    name = models.CharField(max_length=80, blank=False, null=False)
    email = models.CharField(max_length=40, blank=False, null=False)
    company_name = models.CharField(max_length=30, blank=True, null=True)
    country = models.CharField(max_length=2, blank=False, null=False)
    invoice_currency = models.CharField(max_length=3, blank=False, null=False)

    def __str__(self):
        return self.name

    def total_invoiced_last_year(self):
        one_year_ago = timezone.now() - datetime.timedelta(days=365)
        amount_sum_dict = self.invoice_set.filter(date__gt=one_year_ago).aggregate(Sum('amount'))
        return list(amount_sum_dict.values())[0] if amount_sum_dict else 0
