from rest_framework.permissions import BasePermission
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from authapp.models import ApiAdminAction
class AdminAction(BasePermission):
    def has_permission(self, request, view):        
        if request.user.is_superuser:
            return True        
        if request.user.is_authenticated:
            try:                
                api_admin_action = ApiAdminAction.objects.get(user=request.user)

                if api_admin_action.action and request.method in ["PUT", "GET", "POST"]:
                    return True                    
            except ApiAdminAction.DoesNotExist:
                return False
        return False
