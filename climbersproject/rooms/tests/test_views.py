from rest_framework import status
from rest_framework.test import APITestCase

from django.utils.timezone import make_aware

from datetime import datetime

from rooms.models import Room, Membership
from accounts.models import Account

class RoomViewSetTestCase(APITestCase):

    def setUp(self):
        self.room_owner = Account(
            email = 'test_email@emai.com',
            username = 'test_user',
            password = 'test_password',
            weight = 80,
            boulder_grade = '4a',
            lead_grade = '2a',
            toprope_grade = '6')
        self.room_owner.save()

        self.user2 = Account(
            email = 'test_email2@emai.com',
            username = 'test_user2',
            password = 'test_password2',
            weight = 80,
            boulder_grade = '4a',
            lead_grade = '2a',
            toprope_grade = '6')
        self.user2.save()

        self.data_room = {
            'name': 'test_room',
            'description': 'test_description',
            'date': make_aware(datetime.now())}

        self.some_room = Room.objects.create(
            name = 'some_room',
            description = 'some_destcription',
            date = make_aware(datetime.now()))
        self.owner_membership = Membership.objects.create(account=self.room_owner,
            room=self.some_room)
        self.some_room.members.add(self.owner_membership.account)

    def test_get_rooms_list(self):
        response = self.client.get('/rooms/rooms/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_room_detail(self):
        url = '/rooms/rooms/'+ str(self.some_room.id) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_room_create(self):
        self.client.force_authenticate(user=self.room_owner)
        response = self.client.post('/rooms/rooms/', self.data_room)
        self.assertTrue(Room.objects.get(name='test_room'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_room_delete_by_owner(self):
        self.client.force_authenticate(user=self.room_owner)
        url = '/rooms/rooms/'+ str(self.some_room.id) + '/'
        response = self.client.delete(url)
        room = Room.objects.filter(id=self.some_room.id)
        self.assertFalse(room.count())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_room_delete_by_non_owner(self):
        self.client.force_authenticate(user=self.user2)
        url = '/rooms/rooms/'+ str(self.some_room.id) + '/'
        response = self.client.delete(url)
        self.assertTrue(Room.objects.get(id=self.some_room.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_membership(self):
        response = self.client.get('/rooms/memberships/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_membership_by_annonymous_user_returns_401(self):
        response = self.client.post('/rooms/memberships/', data = {
             'room_id': self.some_room.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_membership_by_user(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.post('/rooms/memberships/', data = {
             'room_id': self.some_room.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate_membership_returns_403(self):
        self.client.force_authenticate(user=self.room_owner)
        response = self.client.post('/rooms/memberships/', data = {
             'room_id': self.some_room.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_membership_by_room_owner(self):
        self.regular_membership = Membership.objects.create(account=self.user2,
            room=self.some_room)
        self.some_room.members.add(self.regular_membership.account)
        self.client.force_authenticate(user=self.room_owner)
        url = '/rooms/memberships/'+ str(self.regular_membership.id) + '/'
        response = self.client.delete(url)
        self.assertFalse(Membership.objects.filter(
            id=self.regular_membership.id).count())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_membership_by_membership_owner(self):
        self.regular_membership = Membership.objects.create(account=self.user2,
            room=self.some_room)
        self.some_room.members.add(self.regular_membership.account)
        self.client.force_authenticate(user=self.user2)
        url = '/rooms/memberships/'+ str(self.regular_membership.id) + '/'
        response = self.client.delete(url)
        self.assertFalse(Membership.objects.filter(
            id=self.regular_membership.id).count())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_membership_by_other_user_returns_403(self):
        self.client.force_authenticate(user=self.user2)
        url = '/rooms/memberships/'+ str(self.owner_membership.id) + '/'
        response = self.client.delete(url)
        self.assertTrue(Membership.objects.filter(
            id=self.owner_membership.id).count())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
