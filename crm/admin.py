from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.db.models import Sum
from django.urls import reverse

from .models import User, Invoice


class ThousandAmountListFilter(admin.SimpleListFilter):
    title = _("1000 greater or lesser filter")

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "amount"

    def lookups(self, request, model_admin):
        return [
            ("lte1000", _("Less or equal to 1000")),
            ("gt1000", _("More than 1000")),
        ]

    def queryset(self, request, queryset):
        ta_annotated_users = queryset.annotate(total_amount=Sum('invoice__amount'))
        
        if self.value() == "lte1000":
            return ta_annotated_users.filter(total_amount__lte=1000)
        if self.value() == "gt1000":
            return ta_annotated_users.filter(total_amount__gt=1000)

class InvoiceInline(admin.TabularInline):
    model = Invoice
    extra = 0
    max_num = 3
    can_delete = False
    ordering = ("-date",)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = [ThousandAmountListFilter]

    inlines = [
        InvoiceInline,
    ]

    list_display = ('name', 'email', 'invoice_link', 'total_invoiced_last_year')
    readonly_fields = ('invoice_link', 'total_invoiced_last_year')

    def invoice_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            f'/admin/crm/invoice/?user__name={obj.name}',
            "See all invoices"
        ))
    invoice_link.short_description = 'invoices'



@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_filter = ['user__name']

    list_display = ('invoice_number', 'user_link', )
    readonly_fields = ('user_link',)

    def user_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:crm_user_change", args=(obj.user_id,)),
            obj.user.name
        ))
    user_link.short_description = 'user'

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions
