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
    
    def update(self, instance, validated_data):
        # Verificar se a senha atual foi fornecida para alterar a senha
        if 'password' or 'email' in validated_data:
            current_password = validated_data.pop('current_password', None)

            if not current_password:
                raise serializers.ValidationError({'current_password': 'A senha atual é necessária para atualizar a senha ou o email.'})
            
            if not instance.check_password(current_password):
                raise serializers.ValidationError({'current_password': 'A senha atual está incorreta.'})

            instance.set_password(validated_data['password'])

        # Atualizar outros campos
        for attr, value in validated_data.items():
            if attr != 'password':
                setattr(instance, attr, value)

        instance.save()
        return instance


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
        