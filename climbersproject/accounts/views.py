from rest_framework import viewsets
from rest_framework.response import Response

from . import serializers
from . import models
from . import permissions

class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AccountSerializer
    queryset = models.Account.objects.all()
    permission_classes = (permissions.UpdateOwnAccountPermission, )
