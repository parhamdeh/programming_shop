from payment.models import Payment


def get_payment(payment_id: int) -> Payment:
    return Payment.objects.get(id=payment_id)