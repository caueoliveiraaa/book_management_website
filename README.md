# SISTEMA DE GERENCIAMENTO DE LIVROS E USUÁRIOS.

    # Visão Geral:
        O Sistema de Gerenciamento de Livros é uma aplicação baseada em Django projetada 
        para gerenciar o inventário e as reservas de livros em uma biblioteca online.
        É possível criar, excluir e atualizar entradas de livros. E também é possível
        criar, excluir e atualizar perfis de usuários.

    # Permissões:
        Administradores: Podem criar livros e alterar o status de um livro.
        Usuários: Podem reservar e listar livros.

    # Implantação:
        Crie um ambiente virtual para instalar as dependências. 
        Instale o Django e as dependências necessárias com comando 'pip install -r requirements.txt'.
        Configure as configurações do banco de dados em settings.py.
        Execute as migrações: python manage.py migrate.
        Crie um superusuário para acesso administrativo: python manage.py createsuperuser.
        Inicie o servidor de desenvolvimento: python manage.py runserver.
