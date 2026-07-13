from rest_framework import serializers

from posts.models import Subscription, UserSubscription


class SubscriptionInputSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.IntegerField()
    limit_days = serializers.IntegerField()


class SubscriptionOutputModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class UserSubscriptionOutputSerializer(serializers.ModelSerializer):
    remaining_days = serializers.SerializerMethodField()

    class Meta:
        model = UserSubscription
        fields = "__all__"

    def get_remaining_days(self, obj):
        return obj.remaining_days

