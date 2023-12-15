from rest_framework import serializers
from rest_framework.authtoken.models import Token

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password']

    def save(self, **kwargs):
        new_user = CustomUser.objects.create_user(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            password=self.validated_data['password'],
        )
        new_user.save()














































