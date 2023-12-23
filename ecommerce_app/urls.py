from django.urls import path
from .views import CreateUserView, DeleteUserView, ListUsersView, LoginView, LogoutView, ListProductsView, CreateProductView, UpdateUserView

urlpatterns = [
    path('users/', ListUsersView.as_view(), name='users'),
    path('register/', CreateUserView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('user/update/', UpdateUserView.as_view(), name='user-update'),
    path('user/delete/', DeleteUserView.as_view(), name='user-delete'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('produtos/', ListProductsView.as_view(), name='products'),
    path('produto/create/', CreateProductView.as_view(), name='create_product'),
]
