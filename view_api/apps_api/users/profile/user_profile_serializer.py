from rest_framework import serializers

from view_api.apps_api.posts.post.post_serializers import PostOutputModelSerializer
from view_api.apps_api.posts.subscription.subscription_serializers import SubscriptionOutputModelSerializer, UserSubscriptionOutputSerializer




class ProfileOutputSerializer(serializers.Serializer):
    username = serializers.CharField(source="user.username")
    phone = serializers.CharField(source="user.phone")
    subscription = UserSubscriptionOutputSerializer()
    favorits = PostOutputModelSerializer(many=True)
    
