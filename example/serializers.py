from rest_framework import serializers
from .models import User
from .models import HistoricoTesouro

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'bio']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)



class HistoricoTesouroSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoTesouro
        fields = ['id', 'data_captura', 'payload_cru']