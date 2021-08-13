from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Account

class AccountViewSetTestCase(APITestCase):

    def setUp(self):
        self.user_data = {
            'email': 'test_email2@emai.com',
            'username': 'test_user2',
            'password': 'test_password2',
            'weight': 80,
            'boulder_grade': '4a',
            'lead_grade': '5c',
            'toprope_grade': '5c'}

        self.user = Account(
            email = 'test_email@emai.com',
            username = 'test_user',
            password = 'test_password',
            weight = 80,
            boulder_grade = '4a',
            lead_grade = '2a',
            toprope_grade = '6')
        self.user.save()

        self.user3 = Account(
            email = 'test_email3@emai.com',
            username = 'test_user3',
            password = 'test_password3',
            weight = 80,
            boulder_grade = '4a',
            lead_grade = '2a',
            toprope_grade = '6')
        self.user3.save()

    def test_get_account_list(self):
        response = self.client.get('/accounts/account/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_account_detail(self):
        url = '/accounts/account/'+ str(self.user.id) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_account_create(self):
        response = self.client.post('/accounts/account/', self.user_data)
        self.assertTrue(Account.objects.get(username='test_user2'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_account_patch_own_profile(self):
        self.client.force_authenticate(user=self.user)
        url = '/accounts/account/'+ str(self.user.id) + '/'
        response = self.client.patch(url, {'weight': 70})
        self.assertTrue(Account.objects.get(weight=70))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_account_patch_not_own_profile(self):
        self.client.force_authenticate(user=self.user3)
        url = '/accounts/account/'+ str(self.user.id) + '/'
        response = self.client.patch(url, {'weight': 70})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
