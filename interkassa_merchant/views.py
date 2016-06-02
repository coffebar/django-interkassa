import base64
from hashlib import md5

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import mail_admins
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from interkassa_merchant.forms import NotificationForm, SettledPaymentForm
from interkassa_merchant.models import Invoice, Payment
from interkassa_merchant.signals import interkassa_payment_accepted


@require_POST
@csrf_exempt
def result(request):
    form = NotificationForm(request.POST)
    if not form.is_valid():
        message = 'Invalid Form Data:\n'
        for key in form.errors:
            message += key + ', '.join(form.errors[key]) + '\n'
        mail_admins('Unprocessed request to interkassa merchant',
                    message, fail_silently=True)
        return HttpResponseBadRequest("Invalid Form Data!")

    if form.cleaned_data['ik_act'] not in ('process', ''):
        mail_admins('Unprocessed request to interkassa merchant',
                    'Status: "%s"' % form.cleaned_data['ik_act'], fail_silently=True)
        return HttpResponse("success")

    payment_no = form.cleaned_data['ik_pm_no']
    try:
        invoice = Invoice.objects.get(payment_no=payment_no)
    except ObjectDoesNotExist:
        mail_admins('Unprocessed request to interkassa merchant',
                    'Not found Invoice with payment_no=%s' % payment_no, fail_silently=True)
        return HttpResponseBadRequest("Invalid Invoice ID!")

    data = []
    for x in sorted(request.POST.keys()):
        if x.startswith('ik_') and x != 'ik_sign':
            data.append(str(request.POST.get(x)))
    data.append(settings.INTERKASSA_SECRET)
    sign = base64.b64encode(md5(":".join(data).encode()).digest()).decode()

    if form.cleaned_data['ik_sign'] == sign:
        amount = form.cleaned_data['ik_am']
        if amount != invoice.amount:
            mail_admins('Unprocessed request to interkassa merchant',
                        'Incorrect ik_am=%s for payment_no=%s' % (amount, payment_no),
                        fail_silently=True)
            return HttpResponseBadRequest("Incorrect ik_am")

        if form.cleaned_data['ik_inv_st'] == 'success':
            payment = Payment(amount=amount, invoice=invoice, payment_no=payment_no,
                              ik_pw_via=form.cleaned_data['ik_pw_via'],
                              ik_cur=form.cleaned_data['ik_cur'],
                              ik_inv_prc=form.cleaned_data['ik_inv_prc'])
            payment.save()
            interkassa_payment_accepted.send(sender=payment.__class__, payment=payment)
        else:
            message = 'Status ik_inv_st was %s for payment_no=%s' % (form.cleaned_data['ik_inv_st'],
                                                                     payment_no)
            mail_admins('Unprocessed request to interkassa merchant',
                        message, fail_silently=True)
        return HttpResponse("success")
    else:
        mail_admins('Unprocessed request to interkassa merchant',
                    'Incorrect hash for payment %s.' % payment_no, fail_silently=True)
        return HttpResponseBadRequest("Incorrect hash")


@csrf_exempt
def success(request):
    response = {}
    form = SettledPaymentForm(request.POST)
    if form.is_valid():
        response = form.cleaned_data
    return render(request, 'interkassa_merchant/success.html', response)


@csrf_exempt
def fail(request):
    response = {}
    form = SettledPaymentForm(request.POST)
    if form.is_valid():
        response = form.cleaned_data
    return render(request, 'interkassa_merchant/fail.html', response)


@csrf_exempt
def wait(request):
    return render(request, 'interkassa_merchant/wait.html', {})
