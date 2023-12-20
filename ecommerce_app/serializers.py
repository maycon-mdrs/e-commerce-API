from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import CustomUser, Product

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'phone_number', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            name=validated_data['name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)

        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price', 'quantity', 'image', 'user')
        read_only_fields = ('user',)  # O usuário será definido automaticamente, então não precisa ser fornecido

    def create(self, validated_data):
        # Associa automaticamente o usuário da requisição ao produto
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class VendasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        