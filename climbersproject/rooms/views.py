from rest_framework import viewsets

from . import serializers
from . import models

class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RoomSerializer
    queryset = models.Room.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        """adds current user to validated_data"""
