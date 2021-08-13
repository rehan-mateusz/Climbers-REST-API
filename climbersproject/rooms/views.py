from rest_framework import viewsets, mixins, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from . import serializers
from . import models
from . import permissions

class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RoomSerializer
    queryset = models.Room.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly & permissions.IsRoomOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        """adds current user to validated_data"""

class MembershipListCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.MembershipSerializer
    queryset = models.Membership.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def create(self, serializer):
        if models.Membership.objects.filter(account_id=self.request.user.id,
            room_id=self.request.data['room_id']).count():
            msg = 'User is already a member of this room'
            return Response(msg, status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = self.get_serializer(data=self.request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        room_id=self.request.data['room_id'])

class MembershipDestroyView(mixins.DestroyModelMixin, generics.GenericAPIView):
    permission_classes = [permissions.IsRoomMemberOrOwner,]
    serializer_class = serializers.MembershipSerializer
    queryset = models.Membership.objects.all()
    http_method_names = ['delete']

    def destroy(self, request, *args, **kwargs):
        membership = self.get_object()
        msg = self.perform_destroy(membership)
        return Response(msg, status=status.HTTP_200_OK)

    def perform_destroy(self, membership):
        if membership.room.members.count()==1:
            membership.room.delete()
            return "You have left the room, due to lack of climbers the room has been deleted."
        else:
            membership.delete()
            return "You have left the room."

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
