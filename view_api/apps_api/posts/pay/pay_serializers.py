# Third Party Packages
from rest_framework import serializers


class SubscriptionPaymentOutputSerializer(serializers.Serializer):
    payment_url = serializers.URLField()


class SubscriptionVerifyOutputSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    ref_id = serializers.IntegerField(required=False)
    message = serializers.CharField()