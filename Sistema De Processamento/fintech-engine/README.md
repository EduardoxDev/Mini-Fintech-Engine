<h1 align="center">
  Sistema de Processamento de Transações Financeiras (Fintech Engine)
</h1>

<p align="center">
  <em>Um motor de pagamentos de alta disponibilidade projetado para cenários de missão crítica.</em>
</p>

<p align="center">
  <img alt="Java" src="https://img.shields.io/badge/Java|21-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white" />
  <img alt="Spring Boot" src="https://img.shields.io/badge/Spring_Boot|3.2.4-6DB33F?style=for-the-badge&logo=spring&logoColor=white" />
  <img alt="Architecture" src="https://img.shields.io/badge/Clean_Architecture|Agnostic-blue?style=for-the-badge" />
  <img alt="Resilience4j" src="https://img.shields.io/badge/Resilience4j|Circuit_Breaker-orange?style=for-the-badge" />
  <img alt="Docker" src="https://img.shields.io/badge/Docker|Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
</p>

<hr>

## Sobre o Projeto

O **Fintech Engine** foi desenvolvido para resolver os desafios estruturais e críticos do mercado bancário: consistência absoluta de dados em alta concorrência, tolerância a falhas em integrações externas e proteção agressiva contra abusos em endpoints públicos (APIs).

Construído sob os princípios consolidados do **Domain-Driven Design (DDD)** e **Clean Architecture**, o núcleo financeiro da aplicação (entidades e casos de uso) é rigorosamente isolado da infraestrutura, garantindo testabilidade isolada e evolução de requisitos independente dos frameworks e bancos de dados subjacentes.

## Arquitetura & Padrões Enterprise

A arquitetura do projeto implementa padrões observados em operações de larga escala (High-Frequency Trading e Core Banking):

* **Clean Architecture Estrita:** O pacote `core` contém exclusively código Java Puro. A lógica de negócio dita os contratos (Ports) que a infraestrutura (Adapters) deve cumprir em tempo de execução.
* **Pessimistic Locking de Alta Performance:** Uso nativo de travas de linha nos bancos de dados relacionais (`LockModeType.PESSIMISTIC_WRITE`) para garantir **ACID Compliance** e blindagem total contra *Race Conditions* em atualizações simultâneas de saldo.
* **Transactional Outbox Pattern:** Consolidação de eventos via banco de dados. O processamento transacional (e.g. transferência) registra emissões de eventos (`OutboxEvent`) no mesmo *commit* da operação. Evitam-se assim, falhas distribuídas conhecidas como *Dual-Write*. O sistema fica preparado para o consumo de CDC (Change Data Capture) via ferramentas como Debezium.
* **Circuit Breaker com Resilience4j:** Camada de proteção na integração de serviços instáveis (Ex: provedores externos "Anti-Fraude"). Políticas flexíveis de *Fallback* automáticas (*Half-Open*, *Open* state) isolam falhas sistêmicas e evitam indisponibilidades em cascata ("Snowball Effect").
* **Idempotência Forte (RFC 8946 Approach):** Rastreio imutável via *Headers* `Idempotency-Key`. Retentativas seguras de requisições sobre redes instáveis sem o perigo de dupla dedução (double-spend).
* **Rate Limiting via Token Bucket (Bucket4j):** Componente de segurança alocado na borda da aplicação para prevenir ataques de negação de serviço (DDoS) ou Web Scrapers. Retorna `429 Too Many Requests` aos limitadores configurados.
* **Observabilidade & Instrumentação (Micrometer + Actuator):** Configurações para exportação transparente de métricas da *JVM*, Connection Pools (Hikari), processamento assíncrono e APIs REST. Pronto para ingestão via Prometheus e monitoramento visual detalhado através do Grafana.
* **Migração de Banco de Dados (Flyway):** Controle de versão rigoroso e automatizado da evolução dos esquemas SQL.
* **Problem Details (RFC 7807):** Serialização de respostas a incidentes de rede no formato RESTful padrão global - melhorando substancialmente o consumo inter-sistema para operações B2B.

## Estrutura de Diretórios (Separation of Concerns)

```text
fintech-engine/
 ├── core/                   # Domínio e UseCases (100% Java Puro s/ Spring)
 │   ├── domain/             # Entidades ricas e Value Objects
 │   ├── exception/          # Exceções exclusivas de Regras de Negócio
 │   └── usecase/            # Orquestradores de fluxo (e.g. TransferUseCase)
 ├── infrastructure/         # Tecnologias (Adapters) e configurações Spring
 │   ├── config/             # Configurações transversais (Rate Limiting)
 │   ├── integration/        # Implementações de integrações (Anti-Fraud + Fallbacks)
 │   ├── outbox/             # Modelagem de infraestrutura do Transactional Outbox
 │   └── persistence/        # JpaRepositories, Entities e Lockings explícitos
 └── presentation/           # Camada Lógica Externa (Controllers / REST API)
     └── rest/               # Controladores, Requests, Response e ControllerAdvice
```

## Como Executar

### Requisitos Mínimos:
* Java 21 JDK configurado pontualmente no ambiente (Variável `JAVA_HOME` mapeada).
* Maven (Ou uso nativo da camada do *wrapper* `./mvnw` incluso no projeto).

### Troubleshooting: "JAVA_HOME is not defined correctly"
Caso enfrente este problema ao testar/empacotar, significa que o seu sistema operacional não possui o Java Development Kit (JDK) versão 21 devidamente endereçado na variável global de Path.
1. Efetue o download do [OpenJDK 21](https://jdk.java.net/21/).
2. Defina o endereço de instalação nas "Variáveis de Ambiente" de seu Sistema Operacional sob a chave `JAVA_HOME`.

### Rodando os Testes Unitários
Para validar e empacotar todas as regras arquiteturais, execute o comando raiz:
```bash
./mvnw clean test
```

### Iniciando a Aplicação
Rodará nativamente sob o Tomcat alocado, disponibilizando um banco in-memory H2 transacional imediatamente através do Maven Wrapper:
```bash
./mvnw spring-boot:run
```

## Documentação API (Swagger) & Telemetria

### OpenAPI 3.0 UI
Com a aplicação em funcionamento, usufrua da interface do Swagger para validar as assinaturas estritas, tipagens exigidas nos Modelos e *Endpoints* abertos (como injeções da *Idempotency-Key*):
[http://localhost:8080/swagger-ui/index.html](http://localhost:8080/swagger-ui/index.html)

### Componentes de Monitoramento
As portas do Actuator estão ativas para varreduras de monitoramento (Prometheus Exporter):
[http://localhost:8080/actuator/prometheus](http://localhost:8080/actuator/prometheus)

## Guia Rápido de Uso via cURL

**1. Criação de Conta Operacional**
```bash
curl -X POST http://localhost:8080/api/v1/accounts \
  -H "Content-Type: application/json" \
  -d '{"name": "Conta Matriz", "balance": 100000.00}'
```

**2. Fluxo Transacional (Transação de Pagamento via Identificador)**
```bash
curl -X POST http://localhost:8080/api/v1/transfers \
  -H "Idempotency-Key: cf45e12f-981c-abcf35" \
  -H "Content-Type: application/json" \
  -d '{"sourceId": "UUID-CONTA-A", "targetId": "UUID-CONTA-B", "amount": 850.75}'
```

---
<p align="center">
  Desenvolvido com excelência técnica para sustentar ecossistemas escaláveis de <b>Alta Concorrência</b>.
</p>
