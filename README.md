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
      POSTGRES_USER: "liiink_user"
      POSTGRES_PASSWORD: password
      POSTGRES_DB: "liiink_database"
    volumes:
      - ./data/postgres:/var/lib/postgresql/data
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
