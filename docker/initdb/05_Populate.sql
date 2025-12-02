SET NAMES utf8mb4;

INSERT INTO Medicos (crm, nome_medico, cpf, salario) VALUES
('52341', 'Dr. Lionel Messi', '846.932.810-77', 22500.00),
('58922', 'Dra. Marta Silva', '777.932.040-50', 19800.00),
('61003', 'Dr. Cristiano Ronaldo', '322.232.170-10', 25000.00),
('44201', 'Dra. Megan Rapinoe', '256.487.810-59', 16500.00),
('55100', 'Dr. Neymar Júnior', '805.778.880-13', 18200.00),
('67299', 'Dra. Alex Morgan', '509.248.700-36', 21000.00),
('49881', 'Dr. Kylian Mbappé', '835.351.050-21', 17500.00),
('53444', 'Dra. Formiga', '203.633.860-76', 23000.00);

INSERT INTO TelefoneMedico (crm_medico, numero_telefone) VALUES
('52341', '(61)99988-1001'),
('58922', '(61)98111-2002'),
('61003', '(61)99666-3003'),
('44201', '(61)98222-4004'),
('55100', '(61)99555-5005'),
('67299', '(61)98444-6006'),
('49881', '(61)99333-7007'),
('53444', '(61)98777-8008');

INSERT INTO Enfermeiro (corem, cpf, nome_enfermeiro) VALUES
('DF-1001', '589.101.040-23', 'Enf. Pep Guardiola'),
('DF-1002', '648.437.420-15', 'Enf. Carlo Ancelotti'),
('DF-1003', '065.059.520-39', 'Enf. Jürgen Klopp'),
('DF-1004', '240.336.690-00', 'Enf. José Mourinho'),
('DF-1005', '392.163.520-94', 'Enf. Sir Alex Ferguson');

INSERT INTO TelefoneEnfermeiro (corem_enfermeiro, numero_telefone) VALUES
('DF-1001', '(61)99111-0001'),
('DF-1002', '(61)99222-0002'),
('DF-1003', '(61)99333-0003'),
('DF-1004', '(61)99444-0004'),
('DF-1005', '(61)99555-0005');

INSERT INTO Paciente (cpf, data_nascimento, endereco, nome_paciente, foto) VALUES
('392.163.520-94', '1984-12-30', 'SQS 308 Bloco F, Asa Sul', 'LeBron James', LOAD_FILE('/var/lib/mysql-files/lebron.jpg')),
('619.643.940-58', '1963-02-17', 'SQN 212 Bloco B, Asa Norte', 'Michael Jordan', LOAD_FILE('/var/lib/mysql-files/jordan.jpg')),
('184.021.760-03', '1988-03-14', 'SHIS QI 05 Conjunto 9, Lago Sul', 'Stephen Curry', LOAD_FILE('/var/lib/mysql-files/curry.jpg')),
('254.214.940-20', '1978-08-23', 'Rua das Pitangueiras, Águas Claras', 'Kobe Bryant', LOAD_FILE('/var/lib/mysql-files/kobe.jpg')),
('133.281.290-22', '1972-03-06', 'CCSW 04 Bloco A, Sudoeste', 'Shaquille ONeal', LOAD_FILE('/var/lib/mysql-files/shaq.jpg')),
('097.770.770-92', '1988-07-29', 'QNM 18 Conjunto F, Ceilândia', 'Kevin Durant', LOAD_FILE('/var/lib/mysql-files/durant.jpg')),
('081.844.830-07', '1994-12-06', 'SQS 105 Bloco J, Asa Sul', 'Giannis Antetokounmpo', LOAD_FILE('/var/lib/mysql-files/giannis.jpg')),
('155.272.720-30', '1999-02-28', 'Condomínio Solar de Brasília, Jardim Botânico', 'Luka Dončić', LOAD_FILE('/var/lib/mysql-files/luka.jpg')),
('761.684.990-32', '1959-08-14', 'Avenida Araucárias, Águas Claras', 'Magic Johnson', LOAD_FILE('/var/lib/mysql-files/magic.jpg')),
('517.776.090-11', '1956-12-07', 'SHN Quadra 2, Asa Norte', 'Larry Bird', LOAD_FILE('/var/lib/mysql-files/bird.jpg'));

INSERT INTO TelefonePaciente (id_paciente, numero_telefone) VALUES
(1, '(61)98888-1111'), (2, '(61)98888-2222'), (3, '(61)98888-3333'),
(4, '(61)98888-4444'), (5, '(61)98888-5555'), (6, '(61)98888-6666'),
(7, '(61)98888-7777'), (8, '(61)98888-8888'), (9, '(61)98888-9999'),
(10,'(61)98888-0000');


INSERT INTO AgendaMedico (crm_medico, data, inicio_platao, fim_platao, duracao_slot_minutos) VALUES
('52341', '2025-02-01', '08:00', '12:00', 30),
('58922', '2025-02-01', '14:00', '18:00', 20),
('61003', '2025-02-02', '07:00', '19:00', 60),
('44201', '2025-02-02', '08:00', '14:00', 15),
('55100', '2025-02-03', '10:00', '16:00', 45);


INSERT INTO Consulta (crm_medico, diagnostico, status, valor, data_hora_agendamento, id_paciente) VALUES
('52341', 'Hipertensão Arterial Sistêmica', 'C', 450.00, '2025-01-10 09:00:00', 1),
('58922', 'Amigdalite Bacteriana', 'A', 300.00, '2025-01-12 14:20:00', 2),
('61003', 'Cefaleia Tensional', 'A', 600.00, '2025-01-15 10:00:00', 3),
('44201', 'Dermatite de Contato', 'C', 250.00, '2025-01-18 11:15:00', 4),
('55100', 'Entorse de Tornozelo', 'A', 350.00, '2025-01-20 15:30:00', 5),
('67299', 'Acompanhamento de Rotina', 'A', 200.00, '2025-01-22 08:45:00', 6),
('49881', 'Suspeita de Gastrite', 'A', 280.00, '2025-01-25 13:00:00', 7);


INSERT INTO TipoExame (nome_do_exame, descricao, preco) VALUES
('Hemograma Completo', 'Análise sanguínea completa', 60.00),
('Ressonância Magnética', 'Crânio e Face', 850.00),
('Raio-X', 'Tórax PA e Perfil', 120.00),
('Endoscopia Digestiva', 'Investigação gástrica', 450.00),
('Ecocardiograma', 'Ultrassom do coração', 320.00);

INSERT INTO Exame (status, crm_medico_responsavel, data_coleta, data_solicitacao, id_paciente, id_tipo_exame) VALUES
('C', '52341', '2025-01-11', '2025-01-10', 1, 1),
('C', '61003', '2025-01-16', '2025-01-15', 3, 2),
('A', '55100', NULL, '2025-01-20', 5, 3),
('C', '49881', '2025-01-26', '2025-01-25', 7, 4),
('C', '58922', '2025-01-28', '2025-01-27', 2, 1),
('C', '67299', '2025-01-29', '2025-01-28', 6, 5);

INSERT INTO ResultadoExame (resultado_obtido, data_resultado, id_exame) VALUES
('Leve anemia ferropriva.', '2025-01-13', 1),
('Sem alterações morfológicas significativas.', '2025-01-18', 2),
('Gastrite enantematosa leve de antro.', '2025-01-27', 4),
('Leucocitose leve.', '2025-01-29', 5),
('Função ventricular preservada.', '2025-01-30', 6);

INSERT INTO Procedimento (nome_procedimento, custo, crm_medico, id_paciente) VALUES
('Lavagem Auricular', 150.00, '58922', 2),
('Imobilização Gessada', 250.00, '55100', 5),
('Sutura Simples', 80.00, '44201', 4),
('Curativo Especial', 50.00, '53444', 8),
('Nebulização', 30.00, '58922', 2);

INSERT INTO Quarto (num_quarto, tipo_de_quarto, valor_diaria) VALUES
(101, 'UTI Adulto', 1500.00),
(102, 'UTI Adulto', 1500.00),
(201, 'Duplo', 600.00),
(202, 'Sozinho', 600.00),
(401, 'Berçario', 150.00),
(301, 'Enfermaria', 250.00),
(302, 'Enfermaria', 250.00);

INSERT INTO Internacao (id_paciente, crm_medico, corem_enfermeiro, id_quarto, data_admissao, data_alta_efetiva, data_alta_prevista) VALUES
(1, '52341', 'DF-1001', 3, '2025-01-10', '2025-01-12', '2025-01-12'),
(3, '61003', 'DF-1002', 1, '2025-01-15', NULL, '2025-02-05'),
(5, '55100', 'DF-1003', 2, '2025-01-20', '2025-01-25', '2025-01-25'),
(7, '49881', 'DF-1004', 6, '2025-01-26', NULL, '2025-02-01'),
(2, '58922', 'DF-1005', 4, '2025-01-12', '2025-01-14', '2025-01-14');

INSERT INTO Fornecedor (cnpj, nome_empresa) VALUES
('00.123.456/0001-00', 'Eurofarma Distribuidora DF'),
('99.888.777/0001-99', 'MedQuímica Centro-Oeste'),
('11.222.333/0001-11', 'Bayer S.A.'),
('44.555.666/0001-44', 'Pfizer Brasil'),
('77.888.999/0001-77', 'Novartis Biociências');

INSERT INTO Medicamento (fabricante, nome_comercial) VALUES
('Medley', 'Losartana Potássica 50mg'),
('Aché', 'Deocil SL 10mg'),
('Bayer', 'Aspirina Prevent 100mg'),
('Eurofarma', 'Azitromicina 500mg'),
('Pfizer', 'Dipirona Sódica 500mg');

INSERT INTO EstoqueMedicamento (data_validade, preco_unitario, quantidade, id_medicamento, cnpj_fornecedor) VALUES
('2026-12-31', 5.50, 500, 1, '00.123.456/0001-00'),
('2026-06-30', 22.00, 100, 2, '99.888.777/0001-99'),
('2027-01-01', 8.00, 300, 3, '00.123.456/0001-00'),
('2025-12-01', 15.00, 200, 4, '00.123.456/0001-00'),
('2028-05-20', 3.50, 1000, 5, '44.555.666/0001-44');

INSERT INTO Prescricao (id_consulta, id_medicamento, quantidade_prescrita, dosagem, frequencia_uso) VALUES
(1, 1, 1, '50mg', '1x ao dia pela manhã'),
(5, 2, 1, '10mg', 'Em caso de dor forte (sublingual)'),
(2, 4, 1, '500mg', '1 comprimido por dia por 3 dias'),
(3, 5, 1, '500mg', 'Em caso de febre'),
(4, 3, 1, '100mg', '1 comprimido após o almoço');


INSERT INTO LogSalario (crm_medico, salario_antigo, salario_novo, data_alteracao) VALUES
('52341', 20000.00, 22500.00, '2024-12-01 10:00:00'),
('58922', 18000.00, 19800.00, '2024-12-01 10:00:00'),
('61003', 24000.00, 25000.00, '2024-11-15 09:00:00'),
('44201', 15000.00, 16500.00, '2024-10-01 08:30:00'),
('53444', 21000.00, 23000.00, '2024-12-10 14:00:00');

INSERT INTO Usuarios (username, password, role, referencia_id) VALUES
('admin', 'Adm@DF', 'admin', NULL),
('52341', 'Xy9A2b', 'medico', '52341'),
('58922', 'Kj8L1m', 'medico', '58922'),
('61003', 'Op7R4t', 'medico', '61003'),
('44201', 'Zq2W3e', 'medico', '44201'),
('55100', 'Bn5M6v', 'medico', '55100'),
('67299', 'Qw1E2r', 'medico', '67299'),
('49881', 'Ty3U4i', 'medico', '49881'),
('53444', 'As5D6f', 'medico', '53444'),
('DF-1001', 'Ab12Cd', 'enfermeiro', 'DF-1001'),
('DF-1002', 'Ef34Gh', 'enfermeiro', 'DF-1002'),
('DF-1003', 'Ij56Kl', 'enfermeiro', 'DF-1003'),
('DF-1004', 'Mn7B8v', 'enfermeiro', 'DF-1004'),
('DF-1005', 'Zx9C0v', 'enfermeiro', 'DF-1005');