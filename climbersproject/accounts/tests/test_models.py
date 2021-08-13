from django.test import TestCase

from accounts.models import Account

class AccountTestCase(TestCase):

    def test_create_user(self):
        Account.objects.create_user(
            email = 'test_email@emai.com',
            username = 'test_user',
            password = 'test_password',)
        self.assertTrue(Account.objects.get(username='test_user'))

    def test_create_superuser(self):
        Account.objects.create_superuser(
            email = 'test_email@emai.com',
            username = 'test_user',
            password = 'test_password',)
        self.assertTrue(Account.objects.get(username='test_user'))
