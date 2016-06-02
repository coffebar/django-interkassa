from django.contrib import admin

from interkassa_merchant.models import Invoice, Payment


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['payment_no', 'created_on', 'user', '_is_payed_admin']
    list_filter = ['created_on', 'user']
    date_hierarchy = 'created_on'
    ordering = ['-created_on', 'user']
    search_fields = ['payment_no', 'created_on']
    list_display_links = None

admin.site.register(Invoice, InvoiceAdmin)


class PaymentAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_on'
    list_display = ['payment_no', 'ik_pw_via', 'amount', 'invoice']
    list_filter = ['created_on']
    ordering = ['-created_on']
    search_fields = ['payment_no']

admin.site.register(Payment, PaymentAdmin)
