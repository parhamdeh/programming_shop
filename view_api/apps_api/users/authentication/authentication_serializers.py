# Third Party Packages
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField


class RegisterInputSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    phone = PhoneNumberField(
        region="IR",
    )
    password = serializers.CharField(max_length=128)
    confirm_password = serializers.CharField(max_length=128)

    def validate(self, attrs: dict):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("passwords must be match")
        attrs.pop("confirm_password")
        
        phone = attrs.get("phone")
        if phone and len(str(phone).replace("+98", "0")) > 11:
            raise serializers.ValidationError("phone number is not valid")
        
        attrs["phone"] = str(phone).replace("+98", "0")

        return attrs
    
class VerifyOtpSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)


class RefreshTokenOutputSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    username = serializers.CharField()
    phone = phone = PhoneNumberField(
        region="IR",
    )