# Third Party Packages
from rest_framework import serializers

# Local Apps
from posts.models import FavoritPost


class PostLiksOutputModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoritPost
        fields = "__all__"

