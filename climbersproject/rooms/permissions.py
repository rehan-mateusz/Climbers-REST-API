from rest_framework import permissions

class IsRoomMemberOrOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, membership):

        if membership.account == request.user:
            return True

        else:
            return membership.room.get_owner() == request.user

class IsRoomOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, room):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return room.get_owner() == request.user
