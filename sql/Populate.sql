INSERT INTO Medicos (crm, nome_medico, cpf, salario) VALUES
('123456-SP', 'Dr. João Silva', '123.456.789-01', 15000.00),
('234567-SP', 'Dra. Maria Oliveira', '234.567.890-12', 17000.00),
('345678-SP', 'Dr. Pedro Santos', '345.678.901-23', 16000.00),
('456789-SP', 'Dra. Ana Costa', '456.789.012-34', 15500.00),
('567890-SP', 'Dr. Ricardo Mendes', '567.890.123-45', 18000.00);

INSERT INTO AgendaMedico (crm_medico, data, inicio_platao, fim_platao, duracao_slot_minutos) VALUES
('123456-SP', '2025-01-10', '08:00', '14:00', 30),
('234567-SP', '2025-01-11', '10:00', '18:00', 20),
('345678-SP', '2025-01-12', '07:00', '13:00', 40),
('456789-SP', '2025-01-13', '12:00', '20:00', 30),
('567890-SP', '2025-01-14', '09:00', '17:00', 15);

INSERT INTO Paciente (cpf, data_nascimento, endereco, nome_paciente) VALUES
('111.111.111-11', '1990-05-12', 'Rua A, 100', 'Carlos Pereira'),
('222.222.222-22', '1985-08-30', 'Rua B, 200', 'Fernanda Silva'),
('333.333.333-33', '2000-02-14', 'Rua C, 300', 'Juliana Costa'),
('444.444.444-44', '1978-11-21', 'Rua D, 400', 'Roberto Lima'),
('555.555.555-55', '1995-07-09', 'Rua E, 500', 'Mariana Souza');


INSERT INTO Consulta (crm_medico, diagnostico, status, valor, data_hora_agendamento, id_paciente) VALUES
('123456-SP', 'Gripe', 'A', 150.00, '2025-01-10 09:00:00', 1),
('234567-SP', 'Dor lombar', 'A', 220.00, '2025-01-11 10:30:00', 2),
('345678-SP', 'Alergia', 'C', 180.00, '2025-01-12 08:00:00', 3),
('456789-SP', 'Sinusite', 'A', 210.00, '2025-01-13 14:00:00', 4),
('567890-SP', 'Enxaqueca', 'A', 250.00, '2025-01-14 11:00:00', 5);


INSERT INTO TipoExame (nome_do_exame, descricao, preco) VALUES
('Hemograma', 'Exame de sangue', 50.00),
('Raio-X', 'Imagem do torax', 120.00),
('Ultrassom', 'Abdômen superior', 200.00),
('Glicemia', 'Nível de glicose', 30.00),
('Colesterol', 'Perfil lipídico', 45.00);


INSERT INTO Exame (status, crm_medico_responsavel, data_coleta, data_solicitacao, id_paciente, id_tipo_exame) VALUES
('A', '123456-SP', '2025-01-11', '2025-01-10', 1, 1),
('C', '234567-SP', '2025-01-12', '2025-01-11', 2, 2),
('A', '345678-SP', NULL, '2025-01-12', 3, 3),
('A', '456789-SP', '2025-01-14', '2025-01-13', 4, 4),
('C', '567890-SP', '2025-01-15', '2025-01-14', 5, 5);


INSERT INTO ResultadoExame (resultado_obtido, data_resultado, id_exame) VALUES
('Tudo normal', '2025-01-12', 1),
('Fratura leve detectada', '2025-01-13', 2),
('Sem alterações', '2025-01-14', 3),
('Glicose alta', '2025-01-15', 4),
('Colesterol elevado', '2025-01-16', 5);

INSERT INTO Procedimento (nome_procedimento, custo, crm_medico, id_paciente) VALUES
('Curativo', 80.00, '123456-SP', 1),
('Sutura simples', 150.00, '234567-SP', 2),
('Nebulização', 60.00, '345678-SP', 3),
('Remoção de pontos', 70.00, '456789-SP', 4),
('Pequena drenagem', 200.00, '567890-SP', 5);


INSERT INTO Enfermeiro (corem, cpf, nome_enfermeiro) VALUES
('COREM001', '666.666.666-66', 'Enf. Paula Souza'),
('COREM002', '777.777.777-77', 'Enf. Marcos Dias'),
('COREM003', '888.888.888-88', 'Enf. Carla Nunes'),
('COREM004', '999.999.999-99', 'Enf. Felipe Rocha'),
('COREM005', '101.010.101-01', 'Enf. Helena Prado');


INSERT INTO Quarto (id_quarto, num_quarto, tipo_de_quarto, valor_diaria) VALUES
(1, 101, 'Individual', 300.00),
(2, 102, 'Duplo', 200.00),
(3, 103, 'Coletivo', 150.00),
(4, 104, 'Individual', 320.00),
(5, 105, 'Duplo', 220.00);



INSERT INTO Internacao (id_paciente, crm_medico, corem_enfermeiro, id_quarto, data_admissao, data_alta_efetiva, data_alta_prevista) VALUES
(1, '123456-SP', 'COREM001', 1, '2025-01-01', NULL, '2025-01-10'),
(2, '234567-SP', 'COREM002', 2, '2025-01-02', '2025-01-08', '2025-01-09'),
(3, '345678-SP', 'COREM003', 3, '2025-01-03', NULL, '2025-01-12'),
(4, '456789-SP', 'COREM004', 4, '2025-01-04', NULL, '2025-01-11'),
(5, '567890-SP', 'COREM005', 5, '2025-01-05', '2025-01-15', '2025-01-14');

INSERT INTO Medicamento (fabricante, nome_comercial) VALUES
('Pfizer', 'Ibuprofeno'),
('EMS', 'Dipirona'),
('Aché', 'Amoxicilina'),
('Eurofarma', 'Omeprazol'),
('Takeda', 'Neosaldina');

INSERT INTO Medicamento (fabricante, nome_comercial) VALUES
('Pfizer', 'Ibuprofeno'),
('EMS', 'Dipirona'),
('Aché', 'Amoxicilina'),
('Eurofarma', 'Omeprazol'),
('Takeda', 'Neosaldina');

INSERT INTO Fornecedor (cnpj, nome_empresa) VALUES
('11.111.111/0001-11', 'SaúdeDistribuidora'),
('22.222.222/0001-22', 'FarmaPlus'),
('33.333.333/0001-33', 'BioSuprimentos'),
('44.444.444/0001-44', 'HospitalCare'),
('55.555.555/0001-55', 'MedLogistica');

INSERT INTO EstoqueMedicamento (data_validade, preco_unitario, quantidade, id_medicamento, cnpj_fornecedor) VALUES
('2026-01-10', 10.00, 100, 1, '11.111.111/0001-11'),
('2026-02-15', 5.00, 200, 2, '22.222.222/0001-22'),
('2026-03-20', 12.00, 150, 3, '33.333.333/0001-33'),
('2026-04-25', 8.00, 250, 4, '44.444.444/0001-44'),
('2026-05-30', 18.00, 80, 5, '55.555.555/0001-55');


INSERT INTO TelefoneMedico (crm_medico, numero_telefone) VALUES
('123456-SP', '(11)90000-0001'),
('234567-SP', '(11)90000-0002'),
('345678-SP', '(11)90000-0003'),
('456789-SP', '(11)90000-0004'),
('567890-SP', '(11)90000-0005');

INSERT INTO TelefoneEnfermeiro (corem_enfermeiro, numero_telefone) VALUES
('COREM001', '(11)98888-0001'),
('COREM002', '(11)98888-0002'),
('COREM003', '(11)98888-0003'),
('COREM004', '(11)98888-0004'),
('COREM005', '(11)98888-0005');


INSERT INTO TelefonePaciente (id_paciente, numero_telefone) VALUES
(1, '(11)97777-0001'),
(2, '(11)97777-0002'),
(3, '(11)97777-0003'),
(4, '(11)97777-0004'),
(5, '(11)97777-0005');

INSERT INTO Prescricao (id_consulta, id_medicamento, quantidade_prescrita, dosagem, frequencia_uso) VALUES
(1, 1, 1, '200mg', '2x ao dia'),
(2, 2, 2, '500mg', '3x ao dia'),
(3, 3, 1, '250mg', '1x ao dia'),
(4, 4, 1, '20mg', '1x ao dia'),
(5, 5, 2, '1 comprimido', 'A cada 8h');

