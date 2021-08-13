from django.test import TestCase

from accounts.serializers import AccountSerializer
from accounts.models import Account

class AccountSerializerTestCase(TestCase):

    def setUp(self):
        self.data_valid = {'email': 'test@test.com',
                      'username': 'test_user',
                      'weight': 80,
                      'boulder_grade': '4a',
                      'lead_grade': '5c',
                      'toprope_grade': '5c',
                      'password': 'test_pswd'}
        self.data_invalid = {'email': 'test',
                      'username': 'test_user',
                      'weight': '80aa',
                      'boulder_grade': '4a',
                      'lead_grade': '5c',
                      'toprope_grade': '5c',
                      'password': 'test_pswd'}

    def test_validation_of_invalid_data(self):
        serializer = AccountSerializer(data=self.data_invalid)
        self.assertFalse(serializer.is_valid())

    def test_validation_of_valid_data(self):
        serializer = AccountSerializer(data=self.data_valid)
        self.assertTrue(serializer.is_valid())

    def test_account_create(self):
        serializer = AccountSerializer(data=self.data_valid)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
        else:
            raise ValueError('Provided data is not valid!')
        self.assertTrue(Account.objects.get(username='test_user'))
