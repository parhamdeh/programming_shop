from django.urls import path

from payment.views import StartPaymentView

app_name = "payments"

urlpatterns = [
    path(
        "start/<int:subscription_id>/",
        StartPaymentView.as_view(),
        name="start",
    ),
]