from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import CustomUser, Produto

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'nome', 'numero_telefone', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            nome=validated_data['nome'],
            numero_telefone=validated_data['numero_telefone'],
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

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ('id', 'titulo', 'descricao', 'preco', 'quantidade', 'imagem', 'usuario')
        read_only_fields = ('usuario',)  # O usuário será definido automaticamente, então não precisa ser fornecido

    def create(self, validated_data):
        # Associa automaticamente o usuário da requisição ao produto
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)

class VendasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'
        