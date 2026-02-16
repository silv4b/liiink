# Tecnologias Usadas

Este projeto utiliza as seguintes tecnologias principais:

## Backend

### Django 6.0.2

Framework web Python de alto nível para desenvolvimento rápido de aplicações web seguras e manuteníveis. O Django segue o padrão MTV (Model-Template-View) e inclui:

- ORM nativo para manipulação de banco de dados
- Sistema de autenticação de usuários
- Admin interface automática
- Proteção contra常见 vulnerabilidades (SQL injection, XSS, CSRF)

### Django Allauth 65.14.3

Biblioteca Django para autenticação e gerenciamento de contas de usuários. Suporta:

- Registro/Login com email e senha
- Autenticação social (OAuth)
- Gerenciamento de emails
- Gerenciamento de sessões

### PostgreSQL (psycopg 3.3.2)

Banco de dados relacional robusto e open-source. O projeto utiliza:

- `psycopg` - driver PostgreSQL moderno para Python (versão 3)
- `psycopg2-binary` - driver legacy para compatibilidade

O banco de dados é executado em um container Docker:

```yaml
services:
  postgres14:
    image: postgres:14
    container_name: postgres-14-liiink
    restart: unless-stopped
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: liiink_database
      POSTGRES_USER: liiink_user
      POSTGRES_PASSWORD: password
    volumes:
      - ./data/postgres:/var/lib/postgresql/data

  liiink:
    image: liiink-docker-image:latest
    container_name: liiink-docker-container
    restart: unless-stopped
    ports:
      - "8000:8000"
    depends_on:
      - postgres14
    environment:
      DB_NAME: liiink_database
      DB_USER: liiink_user
      DB_PASSWORD: password
      DB_HOST: 172.17.0.1
      DB_PORT: 5432
```

Para iniciar o banco de dados:

```bash
docker-compose -f docs/docker-compose.yaml up -d
```

### Python Dotenv 1.2.1

Biblioteca para carregar variáveis de ambiente a partir de arquivos `.env`, permitindo configurar a aplicação sem hardcoded credentials.

## Desenvolvimento

### Django Browser Reload 1.21.0

Recarregamento automático do navegador quando arquivos Python ou template mudam durante o desenvolvimento.

### Django Watchfiles 1.4.0

Monitora alterações em arquivos e reinicia automaticamente o servidor de desenvolvimento.

### Watchfiles 1.1.1

Biblioteca de baixo nível que detecta alterações em arquivos em tempo real.

## Estrutura do Projeto

```text
liiink/
├── core/              # Configurações principais do Django
├── links/             # App principal com modelos e views
├── templates/         # Templates HTML
├── static/            # Arquivos estáticos (CSS, JS, imagens)
├── docs/              # Documentação do projeto
├── manage.py          # Script de gerenciamento Django
├── pyproject.toml     # Configuração do projeto
└── .env.example       # Template de variáveis de ambiente
```

## Requisitos

- Python 3.14+
- PostgreSQL 12+

## Padrões de Commits Semânticos

Este projeto utiliza o padrão de **Conventional Commits** para organizar o histórico de alterações. Cada mensagem de commit deve seguir o formato: `<tipo>: <descrição>`

| Tag | Descrição |
| :--- | :--- |
| **feat** | Desenvolvimento de uma nova funcionalidade (ex: novo botão de tema). |
| **fix** | Correção de bugs (ex: erro de contraste no botão primary). |
| **docs** | Alterações em documentações (ex: este README). |
| **style** | Mudanças que não afetam a lógica (espaçamentos, formatação, CSS). |
| **refactor** | Refatoração de código que não altera comportamento nem corrige bug. |
| **perf** | Mudanças de código focadas em melhorar o desempenho. |
| **test** | Adição ou correção de testes. |
| **build** | Mudanças que afetam o sistema de build ou dependências externas. |
| **chore** | Tarefas triviais de manutenção que não mexem no código ou testes. |

## Sobre o uv + poethepoet no Windows

Com o `uv` e o `poethepoet`, para usar comandos facilmente, basta usar `uv run poe <comando_qualquer>`, para comprimir esse comando (considerando a correta configuração do `pyproject.toml`) em apenas `uv`, cole o bloco a seguir no seu profile do Windows Powershell, para isso:

1. No seu windows powershell, execute: `code $profile`.

2. Copie e cole o bloco a seguir:

    ```powershell
    function uv {
        $uvBuiltins = @('add', 'remove', 'sync', 'lock', 'init', 'venv', 'python', 'run', 'tool', 'self', 'help', 'pip')

        if ($args.Count -gt 0 -and $args[0] -notin $uvBuiltins) {
            # Se digitou algo que não é comando nativo do uv, assume que é um comando do Poe.
            & (Get-Command uv -CommandType Application).Source run poe @args
        }
        else {
            # Comandos nativos do uv passam direto
            & (Get-Command uv -CommandType Application).Source @args
        }
    }
    ```

3. Execute: `. $profile` (equivalente ao `sourche .bashrc` ou `source .zshrc` do linux).

4. Teste: `uv dev` para iniciar o servidor django e projeto.
    Deve aparecer algo como:

    ```bash
    PS: D:/caminho/do/projeto> uv dev
    Poe => python manage.py runserver
    Watching for file changes with WatchfilesReloader
    Performing system checks...

    System check identified no issues (0 silenced).
    February 15, 2026 - 13:19:50
    Django version 6.0.2, using settings 'core.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CTRL-BREAK.

    ...
    ```
