# Third Party Packages
from rest_framework_simplejwt.views import TokenObtainPairView

# Local Apps
from .login_serializer import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer