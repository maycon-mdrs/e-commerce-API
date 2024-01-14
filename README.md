# Projeto E-commerce com Django e Django REST Framework

Este projeto é um sistema de e-commerce desenvolvido com Django e Django REST Framework. Ele inclui funcionalidades para gerenciamento de usuários, produtos e vendas, além de autenticação e autorização.

### Tecnologias Utilizadas

- Django
- Django REST Framework
- Pillow
- Django CORS Headers
- Django Extra Fields

### Modelos

- `CustomUser`: Usuário personalizado com campos adicionais.
- `Product`: Modelo para produtos, incluindo título, descrição, preço, quantidade e imagem.
- `Sales`: Modelo para vendas, relacionando produtos, quantidade e usuário.

### Instalação

1. Clone o repositório.
2. Instale as dependências usando `pip install -r requirements.txt`.
3. Configure o banco de dados no arquivo `settings.py`.
4. Execute `python manage.py migrate` para aplicar as migrações.
5. Inicie o servidor com `python manage.py runserver`.

### Front-end
- `Repositório:` https://github.com/maycon-mdrs/e-commerce-admin 

## Endpoints

#### Autenticação

Este projeto utiliza autenticação baseada em token. Após o login, um token é gerado e deve ser utilizado nas requisições subsequentes.

Para os endpoints que requerem autenticação, inclua o seguinte cabeçalho HTTP:
`Headers:`
```bash
{
    Authorization: Token ${token}
}
```


## Usuários

- **Registrar Usuário**  
  `POST /api/register/`  
  ```json
  {
    "name": "Nome",
    "phone_number": "123456789",
    "email": "email@example.com",
    "password": "senha123"
  }
  ```

- **Login**  
  *Retorna um Token de acesso*  
  
  `POST /api/login/`  
  ```json
  {
    "email": "email@example.com",
    "password": "senha123"
  }
  ```

- **Logout**  
  *Requer autenticação*  
  *Não requer JSON* 
  
  `POST /api/logout/`  

- **Atualizar Usuário**  
  *Requer autenticação* 

  `PATCH /api/user/update/`  
  ```json
  {
    "name": "Novo Nome",
    "phone_number": "987654321",
    "current_password": "senha123",
    "password": "novaSenha123"
  }
  ```

- **Deletar Usuário**  
  *Requer autenticação* 

  `DELETE /api/user/delete/`  
  ```json
  {
    "password": "senha123"
  }
  ```


## Produtos

- **Get Produtos**  
  *Requer autenticação*  
  *Não requer JSON* 
  
  `GET /api/produtos/`  

- **Criar Produto**  
  *Requer autenticação*  
  
  `POST /api/produto/create/`  
  ```json
  {
    "title": "Produto",
    "description": "Descrição do Produto",
    "price": 100.0,
    "quantity": 10,
    "image": "data:image/png;base64,..."
  }
  ```

- **Atualizar Produto**  
  *Requer autenticação* 

  `PATCH /api/produto/update/<int:pk>/`  
  ```json
  {
    "title": "Novo Produto",
    "description": "Nova Descrição",
    "price": 150.0,
    "quantity": 5,
    "image": "data:image/jpeg;base64,..."
  }
  ```

- **Deletar Produto**  
  *Requer autenticação*  
  *Não requer JSON* 
  
  `DELETE /api/produto/delete/<int:pk>/`  


## Segurança
- Senhas são armazenadas de forma segura.
- O sistema de autenticação e autorização garante que apenas usuários com permissões adequadas possam acessar ou modificar dados sensíveis.

##

``` python -m venv venv ```
``` .\venv\Scripts\activate ```
``` pip install django ```
``` pip install djangorestframework ```
``` django-admin startproject [name] . ```
``` python manage.py startapp [name] ```
``` python manage.py runserver  ```
``` python manage.py makemigrations ```
``` python manage.py migrate ```
``` python manage.py createsuperuser ```