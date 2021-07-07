from rest_framework import serializers

from . import models

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ['name', 'description', 'date', ]

    def create(self, validated_data):
        new_room = models.Room.objects.create(
            name = validated_data['name'],
            description = validated_data['description'],
            date = validated_data['date'],
            )
        new_membership = models.Membership.objects.create(
            account = validated_data['user'],
            room = new_room
        )
        new_room.members.set([validated_data['user']])
        return new_room
