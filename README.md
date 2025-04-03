# Projeto Agenda (Django)

![Django](https://img.shields.io/badge/Django%204.2LTS-092E20?style=for-the-badge&logo=django&logoColor=white) ![Python](https://img.shields.io/badge/Python%203.11-3776AB?style=for-the-badge&logo=python&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white) ![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white) ![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white)

Uma aplicação web desenvolvida com Django para gerenciamento de contatos pessoais. Permite aos usuários cadastrar, criar, visualizar, editar, buscar e apagar seus contatos, organizando-os por categorias e adicionando fotos.

> **Status:** Em desenvolvimento / Manutenção 

## Funcionalidades Principais

*   **Autenticação de Usuários:** Cadastro, Login e Logout.
*   **Gerenciamento de Perfil:** Atualização de dados do usuário logado.
*   **CRUD de Contatos:**
    *   Criar novos contatos com nome, sobrenome, telefone, email, descrição, categoria e foto.
    *   Visualizar lista de contatos paginada.
    *   Ver detalhes de um contato específico.
    *   Atualizar informações de um contato existente.
    *   Apagar contatos.
*   **Categorias:** Associação de contatos a categorias pré-definidas.
*   **Busca:** Pesquisa de contatos por nome, sobrenome, email ou telefone.
*   **Imagens:** Upload e exibição de fotos para os contatos (usando Pillow).
*   **Interface Administrativa:** Gerenciamento de dados via Admin do Django.
*   **Segurança:** Proteção das views para que apenas usuários logados possam gerenciar seus próprios contatos.

## Tecnologias Utilizadas

*   **Backend:** Python 3.11, Django 4.2 LTS
*   **Banco de Dados:**
    *   **PostgreSQL:** Utilizado no ambiente de **produção/deploy**.
    *   **MySQL:** Configurado para o ambiente de **desenvolvimento local** (conforme instruções abaixo). *Nota: Pode ser adaptado para usar PostgreSQL ou SQLite localmente.*
*   **Servidor WSGI:** Gunicorn
*   **Proxy Reverso / Servidor Web:** Nginx
*   **Frontend:** HTML, CSS (Templates Django)
*   **Infraestrutura de Deploy:** Ubuntu 20.04 LTS (Ex: Google Cloud Compute Engine)
*   **Bibliotecas Principais:**
    *   `psycopg`: Conector PostgreSQL (para produção).
    *   `mysqlclient`: Conector MySQL (para desenvolvimento local, conforme configurado).
    *   `Pillow`: Manipulação de imagens.
    *   `python-dotenv`: Gerenciamento de variáveis de ambiente.
    *   `Faker`: Geração de dados fictícios (para script de população).

## Pré-requisitos (Desenvolvimento Local com MySQL)

*   Python 3.11+ instalado
*   Pip (gerenciador de pacotes Python)
*   Um servidor MySQL rodando e acessível

## Configuração do Ambiente de Desenvolvimento (com MySQL)

Siga os passos abaixo para configurar e rodar o projeto localmente usando MySQL:

1.  **Clone o Repositório:**
    ```bash
    git clone https://github.com/arthurliszkievich/Projeto_Agenda.git
    cd Projeto_Agenda
    ```

2.  **Crie e Ative um Ambiente Virtual:**
    *   **Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    *   **Linux / macOS:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Certifique-se que `requirements.txt` inclua `mysqlclient`)*

4.  **Configure as Variáveis de Ambiente:**
    *   Crie um arquivo chamado `.env` na raiz do projeto.
    *   **IMPORTANTE:** Adicione `.env` ao seu arquivo `.gitignore`!
    *   Adicione as seguintes variáveis, substituindo pelos seus valores:

        ```dotenv
        # .env (Exemplo para Desenvolvimento Local com MySQL)
        SECRET_KEY='sua_chave_secreta_local_aqui'
        DEBUG=True

        # Configurações do Banco de Dados MySQL Local
        DB_NAME='agenda_db'     # Nome do banco de dados local
        DB_USER='agenda_user'   # Usuário do banco local
        DB_PASSWORD='senha_forte' # Senha do usuário local
        DB_HOST='127.0.0.1'     # Host do MySQL local
        DB_PORT='3306'          # Porta do MySQL
        ```

5.  **Configure o Banco de Dados MySQL Local:**
    *   Certifique-se de que seu servidor MySQL local esteja rodando.
    *   Crie um banco de dados e um usuário com as credenciais definidas no `.env`. Exemplo SQL:
        ```sql
        CREATE DATABASE agenda_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        CREATE USER 'agenda_user'@'localhost' IDENTIFIED BY 'senha_forte';
        GRANT ALL PRIVILEGES ON agenda_db.* TO 'agenda_user'@'localhost';
        FLUSH PRIVILEGES;
        ```

6.  **Execute as Migrações:**
    ```bash
    python manage.py migrate
    ```

7.  **(Opcional) Crie um Superusuário:**
    ```bash
    python manage.py createsuperuser
    ```

## Executando a Aplicação (Local)

1.  **Inicie o Servidor de Desenvolvimento Django:**
    ```bash
    python manage.py runserver
    ```

2.  Acesse `http://127.0.0.1:8000/` no seu navegador.

## Nota sobre o Histórico do Banco de Dados

O ambiente de produção configurado para este projeto utiliza **PostgreSQL**. Mensagens de commit mais antigas no histórico do Git podem conter referências incorretas a outros bancos de dados (como MySQL ou SQLite) devido a fases anteriores de desenvolvimento e testes.

## Deploy (Produção)

O deploy deste projeto foi realizado em um servidor Ubuntu 20.04 LTS, utilizando **Nginx** como proxy reverso, **Gunicorn** como servidor WSGI e **PostgreSQL** como banco de dados. A configuração geral envolve:

*   Configuração do servidor Ubuntu.
*   Instalação de dependências (Python 3.11, Nginx, PostgreSQL, Git, etc.).
*   Configuração do banco de dados PostgreSQL (Role e Database).
*   Setup de repositórios Git (bare e checkout).
*   Configuração do ambiente virtual Python e dependências (`psycopg` etc.).
*   Criação de arquivos de serviço Systemd (`.socket` e `.service`) para gerenciar o Gunicorn.
*   Configuração do Nginx (`sites-available`) para servir arquivos estáticos/mídia e fazer proxy para o socket Gunicorn.
*   Configuração do firewall (UFW).
*   (Opcional) Configuração de HTTPS com Certbot.

*(Você pode adicionar mais detalhes ou um link para um guia mais específico aqui, se desejar)*

## (Opcional) Populando com Dados Fictícios

O projeto inclui um script para gerar dados de teste (categorias e contatos) usando a biblioteca Faker.

1.  Execute o script a partir da raiz do projeto (com o ambiente virtual ativo):
    ```bash
    python utils/create_dev_data.py
    ```
    *(Verifique o caminho e nome exato do script)*

2.  Isso pode limpar dados existentes e criar novos dados fictícios.

---

*Sinta-se à vontade para contribuir ou reportar issues!*
