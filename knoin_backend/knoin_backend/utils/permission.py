from rest_framework.permissions import BasePermission


class IsHimself(BasePermission):
    """
    Allows access only to his own data.
    """

    def has_permission(self, request, view):
        user_id = view.kwargs.get('pk')
        return bool(request.user.id == int(user_id))
