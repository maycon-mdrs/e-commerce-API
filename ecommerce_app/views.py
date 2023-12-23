from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from rest_framework.exceptions import PermissionDenied, ValidationError

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from ecommerce_app.models import CustomUser, Product, Sales
from .serializers import CustomUserSerializer, LoginSerializer, ProductSerializer, VendasSerializer

class ListUsersView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(serializer.data)
    
class VerificarTokenByEmailView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        print("Received data:", request.data)
        
        email = request.data.get('email')
        token = request.data.get('token')
        user = CustomUser.objects.get(email=email)

        if user:
            if user.token == token:
                return Response({'message': 'Token válido'})
            else:
                return Response({'error': 'Token inválido'})
        else:
            print(f"Failed login attempt with email: {email}")
            return Response({'error': 'Invalid credentials'})

@method_decorator(csrf_exempt, name='dispatch')
class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        # Sobrescreva o método create para lidar com os dados JSON no corpo da solicitação
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

@method_decorator(csrf_exempt, name='dispatch') 
class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        print("Received data:", request.data)
        
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'name': user.name})
        else:
            print("Failed login attempt with email: {email}")
            return Response({'error': 'Invalid credentials'}, status=403)

class UpdateUserView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated,]

    def get_object(self):
        user = self.request.user
        if not user.is_anonymous:
            return user
        raise PermissionDenied("Você não tem permissão para acessar este recurso.")

class DeleteUserView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated,]

    def delete(self, request, *args, **kwargs):
        user = request.user
        password = request.data.get('password')

        if user.check_password(password):
            user.delete()
            return Response({'message': 'Usuário deletado com sucesso.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError({'password': 'Senha incorreta.'})


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        logout(request)
        return Response({'message': 'Successfully logged out'})


class ListProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Filtra os produtos associados ao usuário autenticado
        return Product.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

class CreateProductView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
    
