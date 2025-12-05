# HospitalGest - Sistema de Gerenciamento Hospitalar

## 📋 Funcionalidades

### 🏥 Portal Médico
* **Agenda Médica:** Visualização de plantões, horários disponíveis e gestão de slots de atendimento.
* **Gestão de Consultas:** Acesso à fila de espera do dia e histórico completo de atendimentos realizados.
* **Prontuário Eletrônico:** Registro de queixas, diagnósticos e visualização do histórico clínico do paciente (consultas e exames anteriores).
* **Prescrição Eletrônica:** Emissão de receitas com baixa automática no estoque da farmácia.
* **Solicitação de Exames:** Pedidos de exames laboratoriais/imagem e visualização de laudos/resultados.

### 👩‍⚕️ Posto de Enfermagem
* **Triagem e Agendamento:** Marcação de novas consultas e realização de internações.
* **Mapa de Leitos:** Visualização em tempo real da ocupação dos quartos (Livre/Ocupado), tipos de leito (UTI, Enfermaria, etc.) e registro de altas.
* **Gestão de Pacientes:** Cadastro completo com upload de foto, dados pessoais e histórico.
* **Farmácia:** Consulta rápida de disponibilidade de insumos e medicamentos.

### ⚙️ Painel Administrativo
* **Gestão de Pessoas:** CRUD completo de Médicos e Enfermeiros com geração automática de usuários de acesso.
* **Estoque e Fornecedores:** Controle de lotes, validade de medicamentos (com alertas de vencimento) e cadastro de fornecedores.
* **Financeiro e Auditoria:** Relatórios de faturamento mensal e logs de auditoria de alterações salariais.
* **Configurações:** Gerenciamento do catálogo de tipos de exames e infraestrutura hospitalar (quartos).

---

## 🛠 Tecnologias Utilizadas

* **Backend:** Python 3, Flask.
* **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript (Vanilla).
* **Banco de Dados:** MySQL 8.0.
* **Infraestrutura:** Docker, Docker Compose.

---

## 🗄️ Estrutura do Banco de Dados

O projeto cumpre os requisitos da disciplina de Banco de Dados, implementando:

### 1. Stored Procedures
* `SP_AgendarConsulta`: Valida a disponibilidade do médico e da agenda antes de confirmar uma consulta.
* `SP_RealizarAltaPaciente`: Processa a alta hospitalar, registrando a data efetiva e liberando o leito.
* `SP_RegistrarResultadoExame`: Atualiza o status do exame e insere os resultados obtidos.

### 2. Triggers
* `TRG_AuditoriaSalario`: Monitora a tabela de Médicos e registra automaticamente qualquer alteração salarial na tabela de Log.
* `TRG_ValidarAltaInternacao`: Garante a integridade dos dados impedindo que a data de alta seja anterior à data de admissão.
* `TRG_SyncMedicoUsuario_Ativo`: Sincroniza o status de "ativo" entre a tabela de Médicos e a tabela de Usuários.
* `TRG_DeleteEnfermeiro_DeleteUsuario`: Remove automaticamente o usuário de acesso ao deletar um enfermeiro.

### 3. Views
* `V_FaturamentoMensal`: Consolida receitas provenientes de consultas e exames, agrupadas por mês e ano.
* `V_HistoricoClinico`: Unifica consultas e exames em uma visão cronológica única para o prontuário do paciente.
* `V_QuartosStatus`: Mapeia a infraestrutura, cruzando dados de quartos, internações ativas e pacientes para indicar ocupação.

### 4. Dados Binários (BLOB)
* Armazenamento e recuperação de fotos dos pacientes diretamente no banco de dados.

---


## 🚀 Como Executar

### Pré-requisitos
* Python 3.x instalado.
* Docker e Docker Compose instalados.

## Passo 1: Subir o Banco de Dados
Utilize o Docker Compose para iniciar o container do MySQL já configurado com os scripts de inicialização:

```bash
docker-compose up --build -d
```
## Passo 2: Configurar a Aplicação (Localmente)

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

## Instalar dependências
```bash
pip install -r requirements.txt
```

## Executar o projeto
```bash
python app.py
```

## Estrutura do Projeto

```
HospitalGest/
├── app.py                  # Arquivo principal da aplicação Flask
├── config/                 # Configurações de conexão (DB)
├── database/               # Classe de conexão e Pool
├── docker/                 # Scripts SQL de inicialização e imagens
│   └── initdb/
│       ├── 01_Script.sql       # Criação das tabelas
│       ├── 02_Views.sql        # Views
│       ├── 03_Procedures.sql   # Stored Procedures
│       ├── 04_Triggers.sql     # Triggers
│       ├── 05_Populate.sql     # Dados iniciais (Seed)
│       └── fotos/              # Imagens para carga inicial
├── repositores/            # Camada de Acesso a Dados (DAO/Repository)
├── routes/                 # Rotas da API e Views (Controllers)
├── services/               # Regras de Negócio
├── static/                 # Arquivos estáticos (CSS, JS)
├── templates/              # Arquivos HTML (Jinja2)
├── utils/                  # Utilitários (ex: gerador de senhas)
├── docker-compose.yml      # Orquestração dos containers
└── requirements.txt        # Dependências Python
```
