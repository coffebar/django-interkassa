from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings


class PaymentRequestForm(forms.Form):
    ik_co_id = forms.CharField(widget=forms.HiddenInput())
    ik_am = forms.DecimalField(max_digits=7, decimal_places=2, widget=forms.HiddenInput())
    ik_desc = forms.CharField(widget=forms.HiddenInput())
    ik_pm_no = forms.IntegerField(widget=forms.HiddenInput())


class BasePaymentForm(forms.Form):
    ik_co_id = forms.CharField()

    def clean_ik_co_id(self):
        if self.cleaned_data['ik_co_id'] != settings.INTERKASSA_ID:
            raise ValidationError("Invalid ik_co_id")
        return self.cleaned_data['ik_co_id']


class ExtraPaymentForm(BasePaymentForm):
    ik_pm_no = forms.IntegerField()
    ik_desc = forms.CharField(required=False)
    ik_cur = forms.CharField(required=False)
    ik_pw_via = forms.CharField(required=False)
    ik_am = forms.DecimalField(max_digits=7, decimal_places=2)


class NotificationForm(ExtraPaymentForm):
    ik_act = forms.CharField(required=False)
    ik_inv_id = forms.IntegerField()
    ik_sign = forms.CharField()
    ik_inv_st = forms.CharField()
    ik_inv_prc = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'])


class SettledPaymentForm(ExtraPaymentForm):
    pass


class UnSettledPaymentForm(ExtraPaymentForm):
    pass
