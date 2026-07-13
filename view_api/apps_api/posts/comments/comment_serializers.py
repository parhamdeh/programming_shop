from rest_framework import serializers
from posts.models import Comments



class PostCommentInputSerializer(serializers.Serializer):
    content = serializers.CharField()


class PostCommentsOutputModelSerializer(serializers.ModelSerializer):
    class Meta:

        model = Comments
        fields = "__all__"


