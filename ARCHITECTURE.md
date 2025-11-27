# Diagrama de Arquitetura

## Visualização do Diagrama

O diagrama de arquitetura está disponível em `architecture.mmd` no formato **Mermaid**.

### Opções para Visualizar

1. **VS Code**: Instale a extensão "Markdown Preview Mermaid Support" ou "Mermaid Preview"
2. **GitHub**: O arquivo `.mmd` será renderizado automaticamente no GitHub
3. **Online**: Use ferramentas como:
   - https://mermaid.live/
   - https://mermaid-js.github.io/mermaid-live-editor/

### Explicação do Diagrama

O diagrama representa a **Arquitetura Hexagonal** do serviço de gerenciamento de pedidos:

- **API Layer (Adapters/HTTP)**: FastAPI recebe requisições HTTP e delega para a camada de aplicação
- **Application Layer**: Use Cases orquestram operações entre domínio e infraestrutura
- **Domain Layer**: Contém entidades (`Order`), value objects (`OrderId`, `Money`, `OrderStatus`) e regras de negócio
- **Ports**: Interfaces que desacoplam o core da infraestrutura (`OrderRepositoryPort`, `MessageBrokerPort`)
- **Adapters**: Implementações concretas (MongoDB, RabbitMQ)
- **Data & Messaging**: MongoDB para persistência e RabbitMQ para eventos

**Fluxo de Atualização de Status**:
1. Cliente faz `PATCH /orders/{id}/status`
2. FastAPI router delega para `UpdateOrderStatusUseCase`
3. Use case busca o pedido via `OrderRepositoryPort` (implementado por `MongoOrderRepository`)
4. Entidade `Order` valida a transição de status (regra de negócio)
5. Pedido é salvo no MongoDB
6. Evento é publicado no RabbitMQ via `MessageBrokerPort` (implementado por `RabbitMQPublisher`)
7. Outros microsserviços podem consumir o evento

**Estratégia de Escalabilidade**:
- **Load Balancer** na frente de múltiplas instâncias da aplicação
- **Réplicas** do MongoDB para alta disponibilidade
- **RabbitMQ Cluster** para mensageria distribuída
- Cada instância da aplicação pode processar requisições independentemente

