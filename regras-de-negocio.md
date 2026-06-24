# Atividade - Arquitetura Hexagonal: Sistema de Consultas Médicas

## Informações Gerais
* **Instituição:** Departamento de Computação - DComp - IFMA
* **Curso:** Sistemas de Informação
* **Disciplina:** Padrões de Software e Refatoração
* **Data de Entrega:** 25/06/2026

## O que se espera com a atividade?
* Entender melhor a Arquitetura Hexagonal.
* Usar os princípios SOLID na prática.
* Usar padrões de projeto de forma consciente.
* Criar código que não dependa de frameworks.
* Preparar o sistema para mudanças no futuro.

## Escopo do Projeto
Você vai criar o módulo de Consultas e Prontuários Médicos para o Dr. Vilegas (pediatra que atende plano de saúde e particular).
O sistema deve seguir a Arquitetura Hexagonal para manter as regras isoladas, com baixo acoplamento e fáceis de testar.

## Modelo de Dados (Diagrama de Classes)
* **Plano de Saúde:** idplano_saude (int), nome_plano (char=100)
* **Telefone:** idendereço (int), numero (char=20), tipo (char=15), idpaciente (int)
* **Paciente:** idpaciente (int), nome_crianca (char=45), nome_responsavel (char=45), data_nasc (int), sexo (char=10), idplano_saude (int), idendereco (int)
* **Endereço:** idendereço (int), logradouro (char=45), numero (char=45), complemento (char=45), bairro (char=45), cidade (char=45), estado (char=45), cep (char=11)
* **Consulta:** idconsulta (int), idpaciente (int), idmedico (int), data_hora (int), novo_paciente (boolean), agendada (boolean)
* **Exame:** idexame (int), nome_exame (char=100)
* **Prontuário:** idprontuario (int), idconsulta (int), peso (double), altura (double), descricao_sintomas (char), observacao_clinica (char)
* **Médico:** idmedico (int), nome_medico (char=45), crm (char=20)
* **Medicamento:** idmedicamento (int), nome_medicamento (int)
* **Prontuário x Exame:** idprontuario (int), idexame (int)
* **Prescrição:** idprescricao (int), idprontuario (int), idmedicamento (int), dosagem (char=45), administracao (char=45), tempo_de_uso (char=45)

## Regras do Sistema
* A secretária agenda as consultas.
* Pacientes novos precisam de: Nome da criança, Nome do responsável, Telefone e Tipo de atendimento.
* Cada consulta gera só um prontuário.
* O prontuário é apenas daquela consulta.
* O prontuário pode ter remédios e exames.
* O sistema deve emitir a receita médica com os remédios, dosagem, tempo de uso, nome e CRM do médico.

## Caso de Uso: Registro de Prontuário
* **Quem faz:** Médico
* **Antes de começar:** Remédios e exames já devem estar cadastrados no sistema.
* **Passos:**
  1. O sistema mostra as consultas do dia (horário, nome, se é paciente novo).
  2. O médico escolhe a consulta.
  3. O sistema abre o prontuário e mostra o histórico de peso e altura.
  4. O sistema mostra a lista de remédios e exames.
  5. O médico preenche: Peso, Altura, Sintomas, Observação, Remédios e Exames.

## Organização da Arquitetura Hexagonal

### 1. Core (Domínio)
Onde ficam as regras do negócio. Não pode usar frameworks ou banco de dados.
* Entidades: Paciente, Consulta, Prontuário, etc.
* Regras: 1 consulta = 1 prontuário. Um prontuário pode ter vários exames e remédios. Um paciente pode ou não ter plano.

### 2. Portas (Interfaces)
* **Entrada:** Casos de uso (exemplo: `RegistrarProntuarioUseCase`).
* **Saída:** Contratos para acessar dados (exemplo: `PacienteRepository`).

### 3. Adaptadores
* **Entrada:** Controllers REST que chamam os casos de uso.
* **Saída:** Código real que salva no banco de dados (exemplo: JPA/Hibernate).

## Etapa 01 - O que você deve fazer (7,0 pontos)
1. Criar o modelo de domínio.
2. Criar os casos de uso.
3. Definir as portas de entrada e saída.
4. Criar os adaptadores.
5. O domínio não pode depender de frameworks.
6. Mostrar que usou a Arquitetura Hexagonal.

## Etapa 02 - Evolução do Sistema (3,0 pontos)
Você precisa criar o código para apenas **duas** destas novas funções. Para as outras, só precisa explicar como faria:
I. Atendimento online (agendamento, histórico, pagamento).
II. Notificações e lembretes.
III. Integração com outros sistemas (exemplo: buscar CRM do médico).
IV. Suporte para mais clínicas e médicos.
V. Sistema de avaliação de atendimento.

*Para cada item, você deve dizer:*
* Quais padrões de projeto usaria.
* Como isso se liga aos princípios SOLID.
* Por que a Arquitetura Hexagonal ajuda nisso.