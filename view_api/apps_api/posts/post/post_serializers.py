from rest_framework import serializers

from posts.models import Post



class PostsInputModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        image = serializers.ImageField(required=False)
        video = serializers.FileField(required=False)
        fields = [
            "title",
            "content",
            "category",
            "image",
            "video",
            "is_premium",
        ]
        extra_kwargs = {
        "image": {"required": False},
        "video": {"required": False},
        }
   

class PostOutputModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [ "title",
                  "id",
            "content",
            "category",
            "image",
            "video",
            "is_premium"]