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
