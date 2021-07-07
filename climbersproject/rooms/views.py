from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from . import serializers
from . import models

class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RoomSerializer
    queryset = models.Room.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        """adds current user to validated_data"""

class MembershipListCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.MembershipSerializer
    queryset = models.Membership.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        room_id=self.request.data['room_id'])
