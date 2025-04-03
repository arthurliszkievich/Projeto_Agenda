# Projeto Agenda (Django)

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

Uma aplicação web desenvolvida com Django para gerenciamento de contatos pessoais. Permite aos usuários cadastrados criar, visualizar, editar, buscar e apagar seus contatos, organizando-os por categorias e adicionando fotos.

## Funcionalidades Principais

*   **Autenticação de Usuários:** Cadastro, Login e Logout.
*   **Gerenciamento de Perfil:** Atualização de dados do usuário logado.
*   **CRUD de Contatos:**
    *   Criar novos contatos com nome, sobrenome, telefone, email, descrição, categoria e foto.
    *   Visualizar lista de contatos paginada.
    *   Ver detalhes de um contato específico.
    *   Atualizar informações de um contato existente.
    *   Apagar contatos.
*   **Categorias:** Associação de contatos a categorias pré-definidas (ex: Amigos, Família).
*   **Busca:** Pesquisa de contatos por nome, sobrenome, email ou telefone.
*   **Imagens:** Upload e exibição de fotos para os contatos.
*   **Interface Administrativa:** Gerenciamento de dados via Admin do Django.
*   **Segurança:** Proteção das views para que apenas usuários logados possam gerenciar seus próprios contatos.

## Tecnologias Utilizadas

*   **Backend:** Python, Django
*   **Banco de Dados:** MySQL (configurado para desenvolvimento)
*   **Frontend:** HTML, CSS (templates Django)
*   **Bibliotecas Principais:**
    *   `mysqlclient`: Conector MySQL para Python/Django.
    *   `Pillow`: Manipulação de imagens.
    *   `python-dotenv`: Gerenciamento de variáveis de ambiente.
    *   `Faker`: Geração de dados fictícios (para script de população).

## Pré-requisitos

*   Python 3.x instalado
*   Pip (gerenciador de pacotes Python)
*   Um servidor MySQL rodando e acessível

## Configuração do Ambiente de Desenvolvimento

Siga os passos abaixo para configurar e rodar o projeto localmente:

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

4.  **Configure as Variáveis de Ambiente:**
    *   Crie um arquivo chamado `.env` na raiz do projeto (mesmo local do `manage.py`).
    *   Copie o conteúdo do arquivo `.env.example` (se existir) ou adicione as seguintes variáveis, substituindo pelos seus valores:

        ```dotenv
        # Exemplo de .env
        SECRET_KEY='sua_chave_secreta_super_segura_aqui'
        DEBUG=True

        # Configurações do Banco de Dados MySQL
        DB_NAME='agenda_db'     # Nome do banco de dados que você criou
        DB_USER='agenda_user'   # Usuário do banco de dados
        DB_PASSWORD='senha_forte' # Senha do usuário do banco
        DB_HOST='127.0.0.1'     # Ou o host onde seu MySQL está rodando
        DB_PORT='3306'          # Porta padrão do MySQL
        ```
    *   **Importante:** A `SECRET_KEY` deve ser única e segura para produção. Você pode gerar uma usando `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`.

5.  **Configure o Banco de Dados MySQL:**
    *   Certifique-se de que seu servidor MySQL esteja rodando.
    *   Crie um banco de dados e um usuário no MySQL com as credenciais que você definiu no arquivo `.env`.
        *   Exemplo (comandos SQL básicos):
            ```sql
            CREATE DATABASE agenda_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
            CREATE USER 'agenda_user'@'localhost' IDENTIFIED BY 'senha_forte';
            GRANT ALL PRIVILEGES ON agenda_db.* TO 'agenda_user'@'localhost';
            FLUSH PRIVILEGES;
            ```
            *(Adapte `localhost` se necessário)*

6.  **Execute as Migrações:**
    ```bash
    python manage.py migrate
    ```
    Isso criará as tabelas necessárias no banco de dados MySQL.

7.  **(Opcional) Crie um Superusuário:**
    ```bash
    python manage.py createsuperuser
    ```
    Siga as instruções para criar um usuário administrador, que pode ser usado para acessar a interface `/admin/`.

## Executando a Aplicação

1.  **Inicie o Servidor de Desenvolvimento:**
    ```bash
    python manage.py runserver
    ```

2.  Abra seu navegador e acesse: `http://127.0.0.1:8000/`

## (Opcional) Populando com Dados Fictícios

O projeto inclui um script para gerar dados de teste (categorias e contatos) usando a biblioteca Faker.

1.  Execute o script a partir da raiz do projeto (com o ambiente virtual ativo):
    ```bash
    python utils/create_dev_data.py
    ```
    *(Certifique-se de que o nome e caminho do script estejam corretos)*

2.  Isso limpará os contatos e categorias existentes e criará novos dados fictícios no banco de dados.

---

*Sinta-se à vontade para contribuir ou reportar issues!*
