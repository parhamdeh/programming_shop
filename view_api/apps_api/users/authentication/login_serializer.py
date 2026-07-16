# Third Party Packages
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Local Apps
from view_api.apps_api.users.user.users_serializer import UserOutputModelSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["phone"] = str(user.phone)

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        data["user"] = UserOutputModelSerializer(self.user).data

        return data