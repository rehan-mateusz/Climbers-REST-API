from django.test import RequestFactory, TestCase
from django.utils.timezone import make_aware

from datetime import datetime

from rooms.permissions import IsRoomMemberOrOwner
from rooms.models import Room, Membership
from accounts.models import Account

class IsRoomMemberOrOwnerTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.permission = IsRoomMemberOrOwner()
        self.room_owner = Account(
            email = 'test_email@emai.com',
            username = 'test_user',
            password = 'test_password',
            weight = 80,
            boulder_grade = '4a',
            lead_grade = '2a',
            toprope_grade = '6')
        self.room_owner.save()

        self.room_member = Account(
            email = 'test_email2@emai.com',
            username = 'test_user2',
            password = 'test_password2',
            weight = 80,
            boulder_grade = '4a',
            lead_grade = '2a',
            toprope_grade = '6')
        self.room_member.save()

        self.non_member = Account(
            email = 'test_email3@emai.com',
            username = 'test_user3',
            password = 'test_password3',
            weight = 80,
            boulder_grade = '4a',
            lead_grade = '2a',
            toprope_grade = '6')
        self.non_member.save()

        self.room = Room.objects.create(
            name = 'test_room',
            description = 'test_destcription',
            date = make_aware(datetime.now()))
        self.owner_membership = Membership.objects.create(account=self.room_owner,
            room=self.room)
        self.room.members.add(self.owner_membership.account)
        self.regular_membership = Membership.objects.create(
            account=self.room_member, room=self.room)
        self.room.members.add(self.regular_membership.account)

    def test_room_owner_can_delete_own_membership(self):
        url = '/rooms/memberships/'+ str(self.owner_membership.id) + '/'
        request = self.factory.delete(url)
        request.user = self.room_owner
        is_permited = self.permission.has_object_permission(request, None,
            self.owner_membership)
        self.assertTrue(is_permited)

    def test_room_owner_can_delete_other_memberships_in_his_room(self):
        url = '/rooms/memberships/'+ str(self.regular_membership.id) + '/'
        request = self.factory.delete(url)
        request.user = self.room_owner
        is_permited = self.permission.has_object_permission(request, None,
            self.regular_membership)
        self.assertTrue(is_permited)

    def test_room_regular_member_can_delete_own_membership(self):
        url = '/rooms/memberships/'+ str(self.regular_membership.id) + '/'
        request = self.factory.delete(url)
        request.user = self.room_member
        is_permited = self.permission.has_object_permission(request, None,
            self.regular_membership)
        self.assertTrue(is_permited)

    def test_room_regular_member_cannot_delete_other_membership(self):
        url = '/rooms/memberships/'+ str(self.owner_membership.id) + '/'
        request = self.factory.delete(url)
        request.user = self.room_member
        is_permited = self.permission.has_object_permission(request, None,
            self.owner_membership)
        self.assertFalse(is_permited)

    def test_non_member_cannot_delete_membership(self):
        url = '/rooms/memberships/'+ str(self.regular_membership.id) + '/'
        request = self.factory.delete(url)
        request.user = self.non_member
        is_permited = self.permission.has_object_permission(request, None,
            self.regular_membership)
        self.assertFalse(is_permited)
