from django.urls import path,re_path

from . import views
from . import api


urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^user/(?P<user_id>\w{0,8})/unpaid_invoices/$', api.UnpaidInvoices.as_view(), name='unpaid_invoices-api')
]