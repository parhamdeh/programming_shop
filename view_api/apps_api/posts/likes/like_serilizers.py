from rest_framework import serializers
from posts.models import FavoritPost


class PostLiksOutputModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoritPost
        fields = "__all__"

