from django.test import TestCase
from django.utils.timezone import make_aware

from datetime import datetime

from rooms.serializers import MembershipSerializer, RoomSerializer
from rooms.models import Room, Membership
from accounts.models import Account

class SerializersTestCase(TestCase):
    def setUp(self):
        self.user = Account(
            email = 'test_email@emai.com',
            username = 'test_user',
            password = 'test_password',
            weight = 80,
            boulder_grade = '4a',
            lead_grade = '2a',
            toprope_grade = '6')
        self.user.save()

        self.data_room = {
            'name': 'test_room',
            'description': 'test_description',
            'date': make_aware(datetime.now())}

        self.some_room = Room.objects.create(
            name = 'some_room',
            description = 'some_destcription',
            date = make_aware(datetime.now()))

    def test_roomserializer_create(self):
        serializer = RoomSerializer(data=self.data_room)
        if serializer.is_valid():
            # serializer.save(user=self.user)
            serializer.validated_data['user'] = self.user
            serializer.create(serializer.validated_data)
        else:
            raise ValueError('Provided data is not valid!')
        self.assertTrue(Room.objects.get(name='test_room'))

    def test_membershipserializer_create(self):
        serializer = MembershipSerializer(data={})
        if serializer.is_valid():
            serializer.validated_data['user'] = self.user
            serializer.validated_data['room_id'] = self.some_room.id
            serializer.create(serializer.validated_data)
        else:
            raise ValueError('Provided data is not valid!')
        self.assertTrue(Membership.objects.get(room_id=self.some_room.id,
            account_id=self.user.id))
