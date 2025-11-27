# Order Management Service

Serviço de gerenciamento de pedidos de e-commerce construído com **FastAPI**, seguindo os princípios de **Domain-Driven Design (DDD)**, **Clean Code** e **Arquitetura Hexagonal (Ports & Adapters)**.

## 📋 Índice

- [Stack Tecnológica](#-stack-tecnológica)
- [Arquitetura](#-arquitetura)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Execução](#-instalação-e-execução)
- [Testes](#-testes)
- [Endpoints](#-endpoints)
- [Decisões Técnicas](#-decisões-técnicas)
- [Diagrama de Arquitetura](#-diagrama-de-arquitetura)

## 🛠 Stack Tecnológica

- **Python 3.11**
- **FastAPI** - Framework web assíncrono
- **Uvicorn** - Servidor ASGI
- **Motor** - Driver assíncrono para MongoDB
- **aio-pika** - Cliente assíncrono para RabbitMQ
- **Pydantic** - Validação de dados
- **structlog** - Logging estruturado
- **pytest** - Framework de testes
- **Docker & Docker Compose** - Containerização

## 🏗 Arquitetura

O projeto segue **Arquitetura Hexagonal (Ports & Adapters)**, separando o código em camadas:

### Domain Layer (Núcleo)
- **Entidades**: `Order` - representa um pedido
- **Value Objects**: `OrderId`, `Money`, `OrderStatus`
- **Exceções de Domínio**: `OrderNotFoundError`, `InvalidStatusTransitionError`
- **Regras de Negócio**: Validação de transições de status

### Application Layer
- **Use Cases**: Orquestração de operações
  - `CreateOrderUseCase`
  - `GetOrderUseCase`
  - `UpdateOrderStatusUseCase`

### Ports (Interfaces)
- `OrderRepositoryPort` - Interface para persistência
- `MessageBrokerPort` - Interface para mensageria

### Adapters (Implementações)
- **HTTP**: FastAPI routers e schemas
- **Persistence**: `MongoOrderRepository` (MongoDB)
- **Messaging**: `RabbitMQPublisher` (RabbitMQ)

## 📁 Estrutura do Projeto

```
.
├── src/
│   ├── domain/              # Camada de domínio
│   │   ├── entities/        # Entidades
│   │   ├── value_objects/   # Value objects
│   │   ├── exceptions/      # Exceções de domínio
│   │   └── ports/           # Interfaces (Ports)
│   ├── application/         # Camada de aplicação
│   │   └── use_cases/       # Casos de uso
│   ├── adapters/            # Adapters (implementações)
│   │   ├── http/           # FastAPI (HTTP adapter)
│   │   ├── persistence/    # MongoDB adapter
│   │   └── messaging/      # RabbitMQ adapter
│   └── app/                 # Configuração e DI
│       ├── main.py         # Aplicação FastAPI
│       ├── config.py       # Configurações
│       └── container.py    # Dependency Injection
├── tests/                   # Testes unitários
├── .github/                 # Configuração do GitHub
│   └── workflows/          # GitHub Actions (CI/CD)
│       └── ci.yml          # Pipeline de CI/CD
├── docker-compose.yml       # Orquestração de serviços
├── Dockerfile              # Imagem da aplicação
├── pyproject.toml          # Configuração do projeto
├── requirements.txt        # Dependências
├── requirements-dev.txt    # Dependências de desenvolvimento
└── README.md              # Este arquivo
```

## 📦 Pré-requisitos

- **Docker** e **Docker Compose** instalados
- **Python 3.11+** (para desenvolvimento local)

## 🚀 Instalação e Execução

### Usando Docker Compose (Recomendado)

1. **Clone o repositório** (se aplicável)

2. **Configure as variáveis de ambiente**:
   ```bash
   cp .env.example .env
   ```
   Edite o `.env` se necessário.

3. **Suba os serviços**:
   ```bash
   docker-compose up --build
   ```

   Isso irá subir:
   - **Aplicação FastAPI** na porta `8000`
   - **MongoDB** na porta `27017`
   - **RabbitMQ** na porta `5672` (Management UI: `15672`)

4. **Acesse a aplicação**:
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - RabbitMQ Management: http://localhost:15672 (guest/guest)

### Execução Local (Desenvolvimento)

1. **Instale as dependências**:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Configure as variáveis de ambiente**:
   ```bash
   cp .env.example .env
   ```

3. **Certifique-se de que MongoDB e RabbitMQ estão rodando** (via docker-compose ou localmente)

4. **Execute a aplicação**:
   ```bash
   uvicorn src.app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## 🧪 Testes

### Executar Testes

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=src --cov-report=term-missing --cov-report=html

# Apenas testes de um módulo
pytest tests/domain/
```

### Cobertura de Testes

O projeto possui **cobertura mínima de 60%** configurada. Para visualizar o relatório:

```bash
pytest --cov=src --cov-report=html
open htmlcov/index.html  # Linux/Mac
# ou navegue até htmlcov/index.html no navegador
```

### Estrutura de Testes

- `tests/domain/` - Testes de entidades e value objects
- `tests/application/` - Testes de use cases (com mocks)
- `tests/adapters/` - Testes de adapters (com mocks)

## 📡 Endpoints

### POST /orders
Cria um novo pedido.

**Request Body**:
```json
{
  "customer_id": "customer-123",
  "items": [
    {
      "product_id": "prod-1",
      "quantity": 2,
      "price": 50.0
    }
  ],
  "total_amount": 100.0
}
```

**Response** (201):
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "customer_id": "customer-123",
  "items": [...],
  "total_amount": {
    "amount": 100.0,
    "currency": "BRL"
  },
  "status": "pending",
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-01T12:00:00"
}
```

### GET /orders/{id}
Obtém um pedido por ID.

**Response** (200):
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  ...
}
```

### PATCH /orders/{id}/status
Atualiza o status de um pedido.

**Request Body**:
```json
{
  "status": "confirmed"
}
```

**Status válidos**: `pending`, `confirmed`, `processing`, `shipped`, `delivered`, `cancelled`

**Nota**: Ao atualizar o status, um evento é publicado no RabbitMQ.

### GET /health
Healthcheck simples.

**Response** (200):
```json
{
  "status": "healthy"
}
```

## 🔧 Decisões Técnicas

### Arquitetura Hexagonal
- **Separação clara** entre domínio, aplicação e infraestrutura
- **Ports (interfaces)** desacoplam o core da infraestrutura
- **Adapters** podem ser trocados sem afetar o domínio

### Domain-Driven Design
- **Entidades** com comportamento (não apenas dados)
- **Value Objects** imutáveis para conceitos do domínio
- **Regras de negócio** no domínio (ex: transições de status)

### Assíncrono
- **FastAPI** com endpoints assíncronos
- **Motor** para MongoDB assíncrono
- **aio-pika** para RabbitMQ assíncrono

### Testes
- **Mocks** para adapters (DB, RabbitMQ)
- **Testes unitários** focados em lógica de negócio
- **Cobertura mínima de 60%**

### Logging
- **structlog** para logs estruturados em JSON
- Facilita integração com sistemas de observabilidade

## 📊 Diagrama de Arquitetura

O diagrama de arquitetura está disponível em `architecture.mmd` (formato Mermaid).

### Explicação do Diagrama

O diagrama representa a arquitetura hexagonal do serviço. A **API Layer** (FastAPI) recebe requisições HTTP e delega para a **Application Layer** (Use Cases), que orquestra operações. O **Domain Layer** contém as entidades e regras de negócio. Os **Ports** definem interfaces que são implementadas pelos **Adapters** (MongoDB e RabbitMQ). Quando o status de um pedido é atualizado, um evento é publicado no RabbitMQ, que pode ser consumido por outros microsserviços. A estratégia de escalabilidade inclui um **Load Balancer** na frente de múltiplas instâncias da aplicação, permitindo escalar horizontalmente.

Para visualizar o diagrama:
- Use um editor que suporte Mermaid (VS Code, GitHub, etc.)
- Ou converta para imagem usando ferramentas online

## 🔍 Linting e Formatação

### Executar Linting

```bash
# Black (formatação)
black src/ tests/

# Ruff (linting)
ruff check src/ tests/

# isort (ordenação de imports)
isort src/ tests/
```

### CI/CD

O projeto utiliza **GitHub Actions** para CI/CD, executando automaticamente:

- ✅ **Verificação de formatação** (Black)
- ✅ **Verificação de ordenação de imports** (isort)
- ✅ **Linting** (Ruff)
- ✅ **Testes** com cobertura mínima de 60%

O pipeline é executado automaticamente em:
- Push para branches `main` e `develop`
- Pull requests para `main` e `develop`

O CI/CD **não utiliza pre-commit**, executando os checks diretamente no pipeline.

## 📝 Variáveis de Ambiente

Veja `.env.example` para todas as variáveis disponíveis:

- `PORT` - Porta da aplicação (padrão: 8000)
- `MONGODB_URL` - URL do MongoDB
- `MONGODB_DB_NAME` - Nome do banco de dados
- `RABBITMQ_URL` - URL do RabbitMQ
- `LOG_LEVEL` - Nível de log (INFO, DEBUG, etc.)

## 🚦 Eventos RabbitMQ

Quando o status de um pedido é atualizado, um evento é publicado no exchange `order_events` com routing key `order.status_updated`:

```json
{
  "order_id": "123e4567-e89b-12d3-a456-426614174000",
  "old_status": "pending",
  "new_status": "confirmed",
  "timestamp": "2024-01-01T12:00:00",
  "event_type": "order.status_updated"
}
```

## 📚 Documentação Adicional

- **Swagger UI**: http://localhost:8000/docs (quando a aplicação estiver rodando)
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contribuindo

1. Siga os padrões de código (Black, Ruff, isort)
2. Mantenha cobertura de testes >= 60%
3. Adicione docstrings para novas funções/classes
4. Use type hints



