# 📄 PDD: API de Gerenciamento Profissional (TaskMaster)

## 1. Visão Geral e Concepção
**Objetivo:** Desenvolver uma API REST robusta para gestão de tarefas e projetos, priorizando a segurança e a integridade dos dados.

**Problema a Resolver:** A falta de ferramentas simples que garantam o isolamento total de dados sensíveis entre usuários, além da carência de métricas rápidas de progresso em fluxos de trabalho comuns.

## 2. Planejamento do Processo de Desenvolvimento
O desenvolvimento será estruturado em fases sequenciais para garantir a qualidade de cada entrega:

1. **Fase de Requisitos:** Mapeamento das entidades (Usuário, Projeto, Tarefa) e definição das regras de negócio fundamentais.
2. **Arquitetura de Dados:** Desenho do Esquema Relacional com foco em Chaves Estrangeiras e integridade referencial.
3. **Draft da API:** Planejamento dos contratos de endpoints utilizando o padrão REST.
4. **Implementação do Core:** Codificação das rotas CRUD e da lógica de persistência.
5. **Camada de Segurança:** Integração de protocolos JWT para blindagem e autorização de acesso.

## 3. Requisitos Técnicos (A Stack)
* **Linguagem:** Python 3.12+ (Foco em legibilidade e suporte a bibliotecas modernas).
* **Framework:** FastAPI (Escolha estratégica pela alta performance e documentação automática via Swagger).
* **ORM:** SQLAlchemy (Para garantir que a lógica do banco de dados seja tratada de forma orientada a objetos).
* **Banco de Dados:** SQLite (Será adotado para garantir portabilidade imediata e facilidade de avaliação em ambiente de portfólio).
* **Segurança:** OAuth2 + JWT (Implementação de tokens *stateless* para garantir escalabilidade).

## 4. Modelagem de Dados Inicial
A estrutura de dados será projetada para suportar uma hierarquia rígida e organizada:

* **User:** O topo da pirâmide e detentor da conta.
* **Project:** Agrupador de objetivos estratégicos (vinculado obrigatoriamente a um `User`).
* **Task:** A unidade mínima de trabalho (vinculada obrigatoriamente a um `Project`).

## 5. Diferenciais de Arquitetura (O "Pensar Diferente")
Dois pilares inegociáveis nortearão todo o desenvolvimento desta solução:

1. **Multi-tenancy Lógico:** O sistema será projetado para filtrar toda e qualquer consulta através do `user_id` da sessão ativa. Esta arquitetura garantirá o isolamento total, impossibilitando tecnicamente qualquer vazamento de dados entre diferentes usuários.
2. **Dashboard Dinâmico:** A API não se limitará a retornar dados brutos; ela deverá processar informações em tempo real para entregar o percentual de saúde de cada projeto (relação entre tarefas concluídas e totais), agregando valor imediato à tomada de decisão.

## 6. Roadmap de Evolução
Como um produto escalável, este PDD prevê futuras iterações após o MVP:

* Migração para PostgreSQL em ambiente de produção.
* Implementação de Docker para padronização de ambiente e conteinerização.
* Criação de níveis de acesso granulares (RBAC: Admin vs. Colaborador).