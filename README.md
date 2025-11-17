# Trabalho_BD

## Configuração do Ambiente Virtual (venv) no Linux

Este guia mostra como configurar um ambiente virtual Python (venv) no Linux.

### Pré-requisitos

Certifique-se de ter o Python 3 instalado no seu sistema. Você pode verificar executando:

```bash
python3 --version
```

Se o Python não estiver instalado, instale-o usando o gerenciador de pacotes da sua distribuição:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

**Fedora:**
```bash
sudo dnf install python3 python3-pip
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip
```

### Passos para Configurar o Ambiente Virtual

#### 1. Clone o Repositório

```bash
git clone https://github.com/ineblinavel/Trabalho_BD.git
cd Trabalho_BD
```

#### 2. Crie o Ambiente Virtual

No diretório do projeto, execute:

```bash
python3 -m venv venv
```

Este comando cria uma pasta chamada `venv` contendo o ambiente virtual.

#### 3. Ative o Ambiente Virtual

Para ativar o ambiente virtual, execute:

```bash
source venv/bin/activate
```

Após a ativação, você verá `(venv)` no início da linha de comando, indicando que o ambiente virtual está ativo.

#### 4. Instale as Dependências

Se o projeto tiver um arquivo `requirements.txt`, instale as dependências com:

```bash
pip install -r requirements.txt
```

#### 5. Desativar o Ambiente Virtual

Quando terminar de trabalhar, você pode desativar o ambiente virtual executando:

```bash
deactivate
```

### Resumo dos Comandos

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências (se houver requirements.txt)
pip install -r requirements.txt

# Desativar ambiente virtual
deactivate
```

### Dicas Importantes

- **Sempre ative o ambiente virtual** antes de instalar pacotes ou executar scripts do projeto.
- O diretório `venv/` não deve ser commitado no git. Adicione-o ao `.gitignore` se necessário.
- Para atualizar o pip dentro do ambiente virtual: `pip install --upgrade pip`
- Para listar pacotes instalados: `pip list`
- Para gerar um novo requirements.txt: `pip freeze > requirements.txt`

### Solução de Problemas

**Erro: "No module named venv"**
```bash
# Ubuntu/Debian
sudo apt install python3-venv
```

**Permissões negadas ao criar venv**
```bash
# Certifique-se de ter permissões de escrita no diretório
ls -la
# Se necessário, ajuste as permissões
chmod u+w .
```

**Ambiente virtual não ativa**
```bash
# Certifique-se de usar 'source' e não 'sh' ou 'bash'
source venv/bin/activate
```
