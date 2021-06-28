from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import filters


from . import serializers
from . import models
from . import permissions

class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AccountSerializer
    queryset = models.Account.objects.all()

    permission_classes = (permissions.UpdateOwnAccountPermission, )

    filter_backends = (filters.SearchFilter, )
    search_fields = ('username')
