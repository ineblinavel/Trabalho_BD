CREATE OR REPLACE VIEW V_FaturamentoMensal AS
        SELECT 
            YEAR(data_hora_agendamento) as ano, 
            MONTH(data_hora_agendamento) as mes, 
            'Consulta' as tipo,
            SUM(valor) as total
        FROM Consulta
        GROUP BY ano, mes
        
        UNION ALL

        SELECT 
            YEAR(e.data_solicitacao) as ano, 
            MONTH(e.data_solicitacao) as mes,
            'Exame' as tipo,
            SUM(te.preco) as total
        FROM Exame e
        JOIN TipoExame te ON e.id_tipo_exame = te.id_tipo_exame
        GROUP BY ano, mes;

CREATE OR REPLACE VIEW V_HistoricoClinico AS
SELECT 
    c.id_paciente,
    c.data_hora_agendamento AS data_evento,
    'Consulta' AS tipo,
    m.nome_medico AS responsavel,
    c.diagnostico AS descricao,
    c.status
FROM Consulta c
JOIN Medicos m ON c.crm_medico = m.crm

UNION ALL

SELECT 
    e.id_paciente,
    e.data_solicitacao AS data_evento,
    CONCAT('Exame: ', te.nome_do_exame) AS tipo,
    m.nome_medico AS responsavel,
    CASE 
        WHEN re.resultado_obtido IS NOT NULL THEN CONCAT('Resultado: ', re.resultado_obtido)
        ELSE 'Aguardando Resultado'
    END AS descricao,
    e.status
FROM Exame e
JOIN Medicos m ON e.crm_medico_responsavel = m.crm
JOIN TipoExame te ON e.id_tipo_exame = te.id_tipo_exame
LEFT JOIN ResultadoExame re ON e.id_exame = re.id_exame;

CREATE OR REPLACE VIEW V_QuartosStatus AS
SELECT 
    q.num_quarto,
    q.tipo_de_quarto,
    q.valor_diaria,
    CASE 
        WHEN i.id_internacao IS NOT NULL THEN 'Ocupado'
        ELSE 'Livre'
    END AS status_atual,
    p.nome_paciente AS paciente_atual
FROM Quarto q
LEFT JOIN Internacao i 
    ON q.id_quarto = i.id_quarto 
    AND i.data_alta_efetiva IS NULL -- Só pega internações ativas
LEFT JOIN Paciente p ON i.id_paciente = p.id_paciente;