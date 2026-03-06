from rest_framework import serializers
from .models import User, Formulario

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


class FormularioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formulario
        fields = ['id', 'user', 'created_at', 'descricao']
        read_only_fields = ['id', 'created_at']
