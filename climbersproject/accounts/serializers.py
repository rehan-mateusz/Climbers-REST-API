from rest_framework import serializers

from . import models

class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Account
        fields = ['email', 'username', 'weight', 'boulder_grade',
            'lead_grade', 'toprope_grade', 'password']
        extra_kwargs = {'password' : {'write_only': True}}

    def create(self, validated_data):

        user = models.Account(
            email=validated_data['email'],
            username=validated_data['username'],
            weight=validated_data['weight'],
            boulder_grade=validated_data['boulder_grade'],
            lead_grade=validated_data['lead_grade'],
            toprope_grade=validated_data['toprope_grade']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
