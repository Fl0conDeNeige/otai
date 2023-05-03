import json

from django.http import HttpResponse
from django.views.generic import View


from .models import Invoice


class UnpaidInvoices(View):
    def get(self, request, user_id, *args, **kwargs):
        unpaid_invoices = Invoice.objects.filter(user__id=user_id).filter(paid=False)
        return HttpResponse(json.dumps([unpaid_inv.invoice_number for unpaid_inv in unpaid_invoices]), content_type='application/json')