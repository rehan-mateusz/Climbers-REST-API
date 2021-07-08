from rest_framework import serializers

from . import models

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ['name', 'description', 'date', 'id']

    def create(self, validated_data):
        new_room = models.Room.objects.create(
            name = validated_data['name'],
            description = validated_data['description'],
            date = validated_data['date'])
        new_membership = models.Membership.objects.create(
            account = validated_data['user'],
            room = new_room)
        new_room.members.set([validated_data['user']])
        return new_room

class MembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Membership
        fields = ['room_id', 'account_id', 'date_joined']

    def create(self, validated_data):
        try:
            new_membership = models.Membership.objects.create(
                account = validated_data['user'],
                room = models.Room.objects.get(id=validated_data['room_id']))
        except:
            raise serializers.ValidationError("User is already a member of this room")
        return new_membership
