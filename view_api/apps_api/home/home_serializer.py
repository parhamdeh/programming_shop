from rest_framework import serializers

from view_api.apps_api.posts.category.category_serializer import CategoryOutputSerializer
from view_api.apps_api.posts.post.post_serializers import PostOutputModelSerializer
from view_api.apps_api.posts.subscription.subscription_serializers import SubscriptionOutputModelSerializer

# posts = get_all_posts()
            # category = get_all_categories()
            # subscription = get_all_subscriptions()

class HomeOutputSerializer(serializers.Serializer):
    post = PostOutputModelSerializer(many=True)
    category = CategoryOutputSerializer(many=True)
    subscription = SubscriptionOutputModelSerializer(many=True)