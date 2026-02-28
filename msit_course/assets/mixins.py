from django.core.exceptions import PermissionDenied

class ManagerOrAdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied('You must be logged in.')
        
        if not request.user.is_manager_or_admin:
            raise PermissionDenied('You must be a Manager or Administrator to perform this action.')
        
        return super().dispatch(request, *args, **kwargs)