
# Evolução do Sistema — Etapa 02

Implementamos no código as funcionalidades **II (Notificações)** e **III (Integração CRM)**. As demais seguem justificativa arquitetural.

## II — Notificações e lembretes (implementado)

- **Padrões:** Observer (`DomainEventListener` + `InProcessEventPublisher`), Gateway (`NotificacaoGateway`).
- **SOLID:** DIP — casos de uso publicam eventos sem conhecer SMS/e-mail; SRP — `ConsoleNotificador` só entrega mensagens.
- **Hexagonal:** eventos no núcleo; adaptador `notifications` traduz para canais externos.

## III — Integração CRM (implementado)

- **Padrões:** Gateway (`MedicoRegistroProfissionalGateway`), Adapter HTTP com `httpx`.
- **SOLID:** ISP — contrato mínimo `validar_crm`; OCP — novos provedores sem alterar domínio.
- **Hexagonal:** porta na aplicação, implementação no adaptador outbound.

## I — Atendimento online (não implementado)

- **Padrões:** Strategy para provedores de videoconferência; State estendido em `Consulta`; Facade para orquestrar agendamento + pagamento.
- **SOLID:** SRP separando pagamento (`PagamentoGateway`); LSP com estratégias intercambiáveis.
- **Hexagonal:** novos adaptadores inbound (webhook de pagamento) e outbound (gateway financeiro) sem tocar entidades.

## IV — Multi-clínicas e médicos (não implementado)

- **Padrões:** Multitenancy via `ClinicaId` em agregados; Repository por contexto; possível Abstract Factory de agendas.
- **SOLID:** OCP — inclusão de clínica por configuração; DIP em repositórios filtrados por tenant.
- **Hexagonal:** filtro de tenant nos adaptadores de persistência, mantendo regras clínicas no domínio.

## V — Avaliação de atendimento (não implementado)

- **Padrões:** Domain Events pós-consulta; CQRS leve (consulta de métricas separada do comando de avaliação).
- **SOLID:** SRP — `RegistrarAvaliacaoUseCase` isolado; ISP — porta `AvaliacaoRepository` enxuta.
- **Hexagonal:** API REST inbound e persistência/analytics outbound plugáveis.
