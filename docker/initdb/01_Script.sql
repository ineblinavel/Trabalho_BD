CREATE TABLE IF NOT EXISTS Medicos (
  crm VARCHAR(9) PRIMARY KEY,
  nome_medico VARCHAR(255) NOT NULL,
  cpf VARCHAR(14) UNIQUE NOT NULL,
  salario DECIMAL(10,2) NOT NULL,
  ativo BOOLEAN DEFAULT TRUE
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS AgendaMedico (
  id_agenda INT AUTO_INCREMENT PRIMARY KEY,
  crm_medico VARCHAR(9) NOT NULL,
  data DATE NOT NULL,
  inicio_platao TIME NOT NULL,
  fim_platao TIME NOT NULL,
  duracao_slot_minutos INT NOT NULL,
  FOREIGN KEY (crm_medico) REFERENCES Medicos (crm)
	ON DELETE CASCADE
    ON UPDATE CASCADE
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS Paciente (
  id_paciente INT AUTO_INCREMENT PRIMARY KEY,
  cpf VARCHAR(14) UNIQUE NOT NULL,
  data_nascimento DATE NOT NULL,
  endereco VARCHAR(255),
  nome_paciente VARCHAR(255) NOT NULL,
  foto LONGBLOB
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS Consulta (
  id_consulta INT AUTO_INCREMENT PRIMARY KEY,
  crm_medico VARCHAR(9),
  diagnostico TEXT,
  status VARCHAR(1),
  valor DECIMAL(10,2),
  data_hora_agendamento DATETIME NOT NULL,
  id_paciente INT NOT NULL,
  FOREIGN KEY (crm_medico) REFERENCES Medicos (crm)
	ON DELETE SET NULL
    ON UPDATE CASCADE,
  FOREIGN KEY (id_paciente) REFERENCES Paciente (id_paciente)
	ON DELETE CASCADE
    ON UPDATE CASCADE
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS TipoExame (
  id_tipo_exame INT AUTO_INCREMENT PRIMARY KEY,
  nome_do_exame VARCHAR(255) NOT NULL,
  descricao VARCHAR(45),
  preco DECIMAL(10,2) NOT NULL
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS Exame (
  id_exame INT AUTO_INCREMENT PRIMARY KEY,
  status VARCHAR(1) NOT NULL,
  crm_medico_responsavel VARCHAR(9) NOT NULL,
  data_coleta DATE,
  data_solicitacao DATE NOT NULL,
  id_paciente INT NOT NULL,
  id_tipo_exame INT NOT NULL,
  FOREIGN KEY (crm_medico_responsavel) REFERENCES Medicos (crm)
	ON DELETE RESTRICT
    ON UPDATE CASCADE,
  FOREIGN KEY (id_paciente) REFERENCES Paciente (id_paciente)
	ON DELETE RESTRICT
    ON UPDATE CASCADE,
  FOREIGN KEY (id_tipo_exame) REFERENCES TipoExame (id_tipo_exame)
	ON DELETE RESTRICT
    ON UPDATE CASCADE
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ResultadoExame (
  id_resultado_exame INT AUTO_INCREMENT PRIMARY KEY,
  resultado_obtido TEXT,
  data_resultado DATE,
  id_exame INT,
  FOREIGN KEY (id_exame) REFERENCES Exame (id_exame)
	ON DELETE CASCADE
    ON UPDATE CASCADE
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS Procedimento (
  id_procedimento INT AUTO_INCREMENT PRIMARY KEY,
  nome_procedimento VARCHAR(255),
  custo DECIMAL(10,2),
  crm_medico VARCHAR(9) NOT NULL,
  id_paciente INT NOT NULL,
  FOREIGN KEY (crm_medico) REFERENCES Medicos (crm)
	ON DELETE RESTRICT
    ON UPDATE CASCADE,
  FOREIGN KEY (id_paciente) REFERENCES Paciente (id_paciente)
	ON DELETE CASCADE
    ON UPDATE CASCADE
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS Enfermeiro (
  corem VARCHAR(15) PRIMARY KEY,
  cpf VARCHAR(14) UNIQUE NOT NULL,
  nome_enfermeiro VARCHAR(255) NOT NULL
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS Quarto (
  id_quarto INT AUTO_INCREMENT PRIMARY KEY,
  num_quarto INT UNIQUE NOT NULL,
  tipo_de_quarto VARCHAR(20) NOT NULL,
  valor_diaria DECIMAL(10,2)
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS Internacao (
  id_internacao INT AUTO_INCREMENT PRIMARY KEY,
  id_paciente INT NOT NULL,
  crm_medico VARCHAR(9) NOT NULL,
  corem_enfermeiro VARCHAR(15) NOT NULL,
  id_quarto INT,
  data_admissao DATE,
  data_alta_efetiva DATE,
  data_alta_prevista DATE,
  FOREIGN KEY (crm_medico) REFERENCES Medicos (crm)
	ON DELETE RESTRICT
    ON UPDATE CASCADE,
  FOREIGN KEY (corem_enfermeiro) REFERENCES Enfermeiro (corem)
	ON DELETE RESTRICT
    ON UPDATE CASCADE,
  FOREIGN KEY (id_quarto) REFERENCES Quarto (id_quarto)
	ON DELETE SET NULL
    ON UPDATE CASCADE,
  FOREIGN KEY (id_paciente) REFERENCES Paciente (id_paciente)
	ON DELETE RESTRICT
    ON UPDATE CASCADE
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS Medicamento (
  id_medicamento INT AUTO_INCREMENT PRIMARY KEY,
  fabricante VARCHAR(45),
  nome_comercial VARCHAR(45)
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS Fornecedor (
  cnpj VARCHAR(18) PRIMARY KEY,
  nome_empresa VARCHAR(255)
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS EstoqueMedicamento (
  id_estoque_medicamento INT AUTO_INCREMENT PRIMARY KEY,
  data_validade DATE NOT NULL,
  preco_unitario DECIMAL(10,2) NOT NULL,
  quantidade INT NOT NULL,
  id_medicamento INT NOT NULL,
  cnpj_fornecedor VARCHAR(18) NOT NULL,
  FOREIGN KEY (id_medicamento) REFERENCES Medicamento (id_medicamento)
	ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY (cnpj_fornecedor) REFERENCES Fornecedor (cnpj)
	ON DELETE CASCADE
    ON UPDATE CASCADE
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS TelefoneMedico (
    id_telefone_medico INT AUTO_INCREMENT PRIMARY KEY,
    crm_medico VARCHAR(9) NOT NULL,
    numero_telefone VARCHAR(15) NOT NULL,
    UNIQUE KEY uk_medico_telefone (crm_medico, numero_telefone), 
    FOREIGN KEY (crm_medico) REFERENCES Medicos (crm)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS TelefoneEnfermeiro (
    id_telefone_enfermeiro INT AUTO_INCREMENT PRIMARY KEY,
    corem_enfermeiro VARCHAR(15) NOT NULL,
    numero_telefone VARCHAR(15) NOT NULL,
    UNIQUE KEY uk_enfermeiro_telefone (corem_enfermeiro, numero_telefone),
    FOREIGN KEY (corem_enfermeiro) REFERENCES Enfermeiro (corem)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS TelefonePaciente (
    id_telefone_paciente INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT NOT NULL,
    numero_telefone VARCHAR(15) NOT NULL,
    UNIQUE KEY uk_paciente_telefone (id_paciente, numero_telefone),
    FOREIGN KEY (id_paciente) REFERENCES Paciente (id_paciente)
        ON DELETE CASCADE 
        ON UPDATE CASCADE
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS Prescricao (
    id_prescricao INT AUTO_INCREMENT PRIMARY KEY,
    id_consulta INT NOT NULL,
    id_medicamento INT NOT NULL,
    quantidade_prescrita INT NOT NULL,
    dosagem VARCHAR(50),
    frequencia_uso VARCHAR(100),
    UNIQUE KEY uk_prescricao (id_consulta, id_medicamento), 
    FOREIGN KEY (id_consulta) REFERENCES Consulta (id_consulta)
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    FOREIGN KEY (id_medicamento) REFERENCES Medicamento (id_medicamento)
        ON DELETE RESTRICT 
        ON UPDATE CASCADE
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS LogSalario (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    crm_medico VARCHAR(9),
    salario_antigo DECIMAL(10,2),
    salario_novo DECIMAL(10,2),
    data_alteracao DATETIME DEFAULT CURRENT_TIMESTAMP
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS Usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL, -- Em produção, usar hash!
    role ENUM('admin', 'medico', 'enfermeiro') NOT NULL,
    referencia_id VARCHAR(15) -- Pode ser CRM, COREM ou NULL (admin)
) DEFAULT CHARSET=utf8mb4;
