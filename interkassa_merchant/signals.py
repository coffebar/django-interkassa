from django.dispatch import Signal

interkassa_payment_accepted = Signal(providing_args=["payment"])
