from django.urls import path
from .views import CreateUserView, ListUsersView, LoginView, LogoutView, ListProductsView, CreateProductView

urlpatterns = [
    path('users/', ListUsersView.as_view(), name='users'),
    path('register/', CreateUserView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('produtos/', ListProductsView.as_view(), name='products'),
    path('produto/create/', CreateProductView.as_view(), name='create_product'),
]
