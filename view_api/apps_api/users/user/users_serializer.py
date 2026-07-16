# Third Party Packages
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

# Local Apps
from users.models import BaseUserModel
from utils.validators import LetterValidator, NumberValidator, SpecialCharValidator


class UserInputSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    phone = PhoneNumberField(
        region="IR",
    )
    password = serializers.CharField(max_length=128, validators=[LetterValidator(), NumberValidator(), SpecialCharValidator()])

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
