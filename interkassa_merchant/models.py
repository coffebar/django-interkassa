import random
from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, models, transaction
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Invoice(models.Model):
    user = models.ForeignKey('auth.User', verbose_name=_("User"), editable=False)
    created_on = models.DateTimeField(_("Created on"), unique=True, editable=False, auto_now_add=True)
    payment_no = models.PositiveIntegerField(_("Payment on"), unique=True, editable=False)
    payment_info = models.CharField(_("Payment Info"), editable=False, max_length=128)
    amount = models.DecimalField(_('Amount'), max_digits=9, decimal_places=2)

    class Meta:
        verbose_name = _("invoice")
        verbose_name_plural = _("invoices")

    def _is_payed_admin(self):
        try:
            self.payment
        except ObjectDoesNotExist:
            return False
        else:
            return True

    _is_payed_admin.boolean = True
    _is_payed_admin.short_description = _('is payed')
    _is_payed_admin.admin_order_field = _('payment')

    is_payed = property(_is_payed_admin)

    @classmethod
    def remove_old(cls, days):
        cls.objects.filter(created_on__lt=timezone.now() - timedelta(days=days), payment__isnull=True).delete()

    def save(self, *args, **kwargs):
        sid = transaction.savepoint()
        if self.pk is None:
            i = 1
            while self.pk is None:

                # Protection from infinite loop
                if i > 20:
                    raise IntegrityError('Too many iterations while generating unique Invoice number.')

                self.payment_no = random.randint(1, 2147483646)

                try:
                    super(Invoice, self).save(*args, **kwargs)
                except IntegrityError:
                    transaction.savepoint_rollback(sid)

                i += 1
        else:
            super(Invoice, self).save(*args, **kwargs)

        transaction.savepoint_commit(sid)
        transaction.commit()

    def __str__(self):
        return _('%(payment_no)s/%(created_on)s (for: %(user)s)') % {'payment_no': self.payment_no,
                                                                     'created_on': self.created_on.date(),
                                                                     'user': self.user}


class Payment(models.Model):
    created_on = models.DateTimeField(_('Created on'), auto_now_add=True, editable=False)
    invoice = models.OneToOneField(Invoice, blank=True, null=True, related_name='payment', verbose_name=_('Invoice'))
    amount = models.DecimalField(_('Amount'), decimal_places=2, max_digits=9)
    payment_no = models.PositiveIntegerField(_('Payment no'), unique=True)
    ik_pw_via = models.CharField(_('Payway Via'), max_length=255)
    ik_cur = models.CharField(_('Currency'), max_length=3)
    ik_inv_prc = models.DateTimeField(_('Invoice Processed'))

    class Meta:
        verbose_name = _("payment")
        verbose_name_plural = _("payments")

    def __str__(self):
        return _("%(payment_no)s - %(amount)s") % {'payment_no': self.payment_no, 'amount': self.amount}
