from django.test import TestCase
from django.utils.timezone import make_aware

from datetime import datetime

from rooms.models import Room, Membership
from accounts.models import Account

class RoomTestCase(TestCase):

    def setUp(self):
        self.user1 = Account(
            email = 'test_email@emai.com',
            username = 'test_user',
            password = 'test_password',
            weight = 80,
            boulder_grade = '4a',
            lead_grade = '2a',
            toprope_grade = '6')
        self.user1.save()
        self.user2 = Account(
            email = 'test_email2@emai.com',
            username = 'test_user2',
            password = 'test_password2',
            weight = 80,
            boulder_grade = '4a',
            lead_grade = '2a',
            toprope_grade = '6')
        self.user2.save()

    def test_create_room(self):
        room = Room.objects.create(
            name = 'test_room',
            description = 'test_destcription',
            date = make_aware(datetime.now()))
        self.assertTrue(room)

    def test_create_membership(self):
        room = Room.objects.create(
            name = 'test_room',
            description = 'test_destcription',
            date = make_aware(datetime.now()))
        membership = Membership.objects.create(account=self.user1, room=room)
        room.members.add(membership.account)
        self.assertTrue(membership)

    def test_room_get_owner(self):
        room = Room.objects.create(
            name = 'test_room',
            description = 'test_destcription',
            date = make_aware(datetime.now()))
        membership1 = Membership.objects.create(account=self.user1, room=room)
        membership2 = Membership.objects.create(account=self.user2, room=room)
        room.members.add(membership1.account, membership2.account)
        self.assertEqual(membership1.account, room.get_owner())

    def test_room_str(self):
        room = Room.objects.create(
            name = 'test_room',
            description = 'test_destcription',
            date = make_aware(datetime.now()))
        self.assertEqual(str(room), room.name)
