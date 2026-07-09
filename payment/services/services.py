from payment.models import Payment


def create_payment(*, user, subscription) -> Payment:
    return Payment.objects.create(
        user=user,
        subscription=subscription,
        amount=subscription.price,
    )