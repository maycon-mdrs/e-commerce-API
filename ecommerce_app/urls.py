from django.urls import path
from .views import CreateUserView, ListUsersView, LoginView, LogoutView, ListProdutosView, CreateProdutoView

urlpatterns = [
    path('users/', ListUsersView.as_view(), name='users'),
    path('register/', CreateUserView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('produtos/', ListProdutosView.as_view(), name='produto'),
    path('produto/create/', CreateProdutoView.as_view(), name='create_produto'),
]
