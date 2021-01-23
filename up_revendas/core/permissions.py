from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsStoreManager(BasePermission):
    """
    Allows access only to store manager users.
    """

    def has_permission(self, request, view):
        # return bool(request.user and (request.user.is_staff or request.user.is_store_manager))
        return bool(
            request.user and ((request.user.is_employee and request.method in SAFE_METHODS)
                              or request.user.is_store_manager))
