from rest_framework import serializers

from . import models

class MembershipSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source = 'account.username')

    class Meta:
        model = models.Membership
        fields = ['room_id', 'date_joined', 'username']

    def create(self, validated_data):
        new_membership = models.Membership.objects.create(
            account = validated_data['user'],
            room = models.Room.objects.get(id=validated_data['room_id']))
        return new_membership

class RoomSerializer(serializers.ModelSerializer):
    members = MembershipSerializer(read_only=True, many=True, source='membership_set')
    class Meta:
        model = models.Room
        fields = ['name', 'description', 'date', 'id', 'members']

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
