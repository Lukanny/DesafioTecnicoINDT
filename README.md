# Sistema de Gerenciamento de Usuários

Este é um sistema completo de gerenciamento de usuários desenvolvido com **Flask** (backend) e **React.js** (frontend), utilizando **SQLAlchemy**, **PostgreSQL**, **Pydantic** e **Docker** para containerização. O sistema permite registro, login, gerenciamento de usuários e visualização de estatísticas.

## Funcionalidades

- **Autenticação de Usuários:** Registro e login com níveis de acesso (comum e admin).
- **CRUD de Usuários:** Administradores podem criar, ler, atualizar e deletar usuários.
- **Painel Administrativo:** Visualização de listas de usuários e estatísticas com gráficos.
- **Gráficos Interativos:** Utilização de D3.js para exibição de dados.
- **Containerização com Docker:** Facilita o ambiente de desenvolvimento e implantação.
- **Migrations e Seeds:** Automatiza a criação e populamento da base de dados.
- **Validação com Pydantic:** Garantia de integridade dos dados.

## Tecnologias Utilizadas

- **Backend:**
  - Flask
  - SQLAlchemy
  - PostgreSQL
  - Pydantic
  - Flask-JWT-Extended
  - Flask-Migrate
  - Flask-RESTX
  - Docker

- **Frontend:**
  - React.js
  - React Router DOM
  - Axios
  - D3.js
  - Docker
  - Nginx

## Para rodar a aplicação:

- **Configuração:**
  - api/.env:
  - SECRET_KEY=supersecretkey
  - JWT_SECRET_KEY=superjwtsecret
  - DATABASE_URI=postgresql://user:password@db:5432/mydb

  - interface/.env:
  - REACT_APP_API_URL=http://localhost:5000/api

- **Para subir as aplicações**:

  - docker compose up --build
  - Entre no container e rode os seguintes comandos:
  - flask db init
  - flask db migrate -m "Initial migration."
  - flask db upgrade
  - python seeds/seed.py

  - Credenciais Admin:
  - admin@example.com
  - adminpassword
