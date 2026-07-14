from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from django.utils import timezone
from posts.models import UserSubscription


class ProfilePermission(BasePermission):
    message = "You do not have permission to modify this profile."

    def has_permission(self, request: Request, view: APIView) -> bool:
        user_id = view.kwargs.get("user_id")

        return (
            request.user.is_authenticated
            and request.user.id == user_id
        )

class IsAdminOrReadOnly(BasePermission):
    """
    permission class for ProductUpdateRetrieveDestroy, ProductListCreate endpoints APIView ->
    if request.user.is_staff = True user can create product, change details or delete it.
    """
    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method.lower() == "get":
            return True
        
        if request.user.is_staff:
            return True
        
        return False
    
class UserChangeIfAdminOrSelfUser(BasePermission):
    """
    permission class for UserUpdateRetrieveDestroy APIView ->
    if user.id = user_id user can change details or delete it 
    """
    def has_permission(self, request: Request, view: APIView) -> bool:
        user_id = view.kwargs.get("user_id")

        if request.user.is_staff:
            return True
        
        return (
            request.user.is_authenticated
            and request.user.id == user_id
        )
    
class PremiumPostPermission(BasePermission):

    message = "Active subscription required."

    def has_object_permission(self, request: Request, view: APIView, obj) -> bool:
        if request.user.is_staff:
            return True
        
        if request.method.lower() == "get":

            if not obj.is_premium:
                return True

            return UserSubscription.objects.filter(
                user=request.user,
                is_active=True,
                end_date__gt=timezone.now(),
            ).exists()
        
        return False
    

class BuySubscriptionPermission(BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj) -> bool:
        if request.user.is_staff:
            return True
        
        if request.method.lower() == "get":
            user_subscription = UserSubscription.objects.filter(
                user=request.user,
                is_active=True,
                end_date__gt=timezone.now(),
            ).exists()
            if not user_subscription:
                return True

        return False
    
