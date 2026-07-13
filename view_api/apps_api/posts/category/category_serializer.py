from rest_framework import serializers
from posts.models import Category



class CategoryInputSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Category
        fields = (
            "name",
            "parent",
        )


class CategoryOutputSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    parent = serializers.StringRelatedField()

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "parent",
            "children",
        )

    def get_children(self, obj):
        return CategoryOutputSerializer(
            obj.children.all(),
            many=True,
        ).data