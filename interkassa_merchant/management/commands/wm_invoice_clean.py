from optparse import make_option

from django.core.management.base import BaseCommand

from interkassa_merchant.models import Invoice


class Command(BaseCommand):
    help = "Clean unpaid invoices older than 'n' day."
    option_list = (
        make_option('--days', '-d', default=30, action='store', type='int', dest='name', help='days period'),
    )

    def handle(self, *labels, **options):
        Invoice.remove_old(options['days'])
