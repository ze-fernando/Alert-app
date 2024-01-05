# Django Notification API

Esta é uma API em Django para gerenciamento de notificações por meio de um sistema de tarefas (tasks). A API oferece rotas para cadastrar usuários, fazer login, cadastrar tarefas, deletar tarefas e editar tarefas. Cada usuario pode ter no máximo 3 tarefas

## Funcionalidades

- Cadastro de Usuários: Rota para cadastrar usuários com nome, e-mail e senha.

- Login de Usuários: Rota para autenticar usuários.

- Cadastro de Tarefas: Rota para cadastrar tarefas com descrição, data de criação automática, hora de envio e usuário atribuído.

- Deletar Tarefa: Rota para deletar uma tarefa existente.

- Editar Tarefa: Rota para editar informações de uma tarefa existente.

- Testes Unitários: Incluídos testes unitários para os modelos `User` e `Task`.

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/django-notification-api.git
   ```
2. Navegue para o diretório do projeto:
    ```bash 
    cd django-notification-api
    ```
3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
4. Execute as migrações:
    ```bash 
    python manage.py migrate
    ```
5. Execute os testes:
    ```bash
    python manage.py test
    ```
6. Inicie o servidor:
    ```bash
    python manage.py runserver
    ```

Acesse a API em [http://localhost:8000/](http://localhost:8000/v1/)

1. Cadastro de Usuários:
http://localhost:8000/v1/signup
```json
{
  "name": "Zeca",
  "password": "senh4ad0r3iz3c4",
  "email": "zeca@example.com"
}
```

2. Login de Usuários:
http://localhost:8000/v1/singin
```json
{
  "name": "Zeca",
  "password": "senh4ad0r3iz3c4"
}
```

3. Cadastro de Tarefas:
http://localhost:8000/v1/task
```json
{
  "task": "Jogar bola",
  "hour": "16:00",
  "user": 1
}
```

4. Deletar Tarefa:
http://localhost:8000/v1/del/{id}


5. Editar Tarefa:
http://localhost:8000/v1/edit/{id}
```json
{
  "task": "Academia",
  "hour": "18:50"
}
```

6. Ver Tarefa:
GET http://localhost:8000/v1/tasks