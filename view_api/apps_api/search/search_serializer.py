from rest_framework import serializers


class PostSearchOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    is_premium = serializers.BooleanField()
    category = serializers.DictField()
    author = serializers.DictField()