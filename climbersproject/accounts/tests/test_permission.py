from django.test import RequestFactory, TestCase

from accounts.permissions import UpdateOwnAccountPermission
from accounts.models import Account

class UpdateOwnAccountPermissionTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = Account(
            email = 'test_email@emai.com',
            username = 'test_user',
            password = 'test_password',
            weight = 80,
            boulder_grade = '4a',
            lead_grade = '2a',
            toprope_grade = '6')
        self.user.save()

        self.user2 = Account(
            email = 'test_email2@emai.com',
            username = 'test_user2',
            password = 'test_password2',
            weight = 80,
            boulder_grade = '4a',
            lead_grade = '2a',
            toprope_grade = '6')
        self.user2.save()


    def test_owner_delete_returns_true(self):
        url = '/accounts/account/'+ str(self.user.id) + '/'
        request = self.factory.delete(url)
        request.user = self.user
        permission = UpdateOwnAccountPermission()
        is_permited = permission.has_object_permission(request, None,
            obj = self.user)
        self.assertTrue(is_permited)

    def test_non_owner_delete_returns_false(self):
        url = '/accounts/account/'+ str(self.user.id) + '/'
        request = self.factory.delete(url)
        request.user = self.user2
        permission = UpdateOwnAccountPermission()
        is_permited = permission.has_object_permission(request, None,
            obj = self.user)
        self.assertFalse(is_permited)
