from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from users.models import BaseUserModel

class UserInputSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    phone = PhoneNumberField(
        region="IR",
    )
    password = serializers.CharField(max_length=128)

    def validate(self, attrs: dict):
        
        phone = attrs.get("phone")
        if phone and len(str(phone).replace("+98", "0")) > 11:
            raise serializers.ValidationError("phone number is not valid")
        
        attrs["phone"] = str(phone).replace("+98", "0")

        return attrs
    

class UserOutputModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUserModel
        exclude = ("password"),
