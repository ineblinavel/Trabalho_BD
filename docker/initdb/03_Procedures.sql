DELIMITER $$

CREATE PROCEDURE SP_AgendarConsulta(
    IN p_crm VARCHAR(9),
    IN p_id_paciente INT,
    IN p_data_hora DATETIME
)
BEGIN
    DECLARE v_conflito INT;

    SELECT COUNT(*) INTO v_conflito
    FROM Consulta
    WHERE crm_medico = p_crm
      AND data_hora_agendamento = p_data_hora
      AND status != 'C';

    IF v_conflito > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: Médico indisponível neste horário.';
    ELSE
        INSERT INTO Consulta (crm_medico, id_paciente, data_hora_agendamento, status, valor)
        VALUES (p_crm, p_id_paciente, p_data_hora, 'A', 150.00);
    END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE SP_RegistrarResultadoExame(
    IN p_id_exame INT,
    IN p_resultado TEXT,
    IN p_data_resultado DATE
)
BEGIN
    INSERT INTO ResultadoExame (id_exame, resultado_obtido, data_resultado)
    VALUES (p_id_exame, p_resultado, p_data_resultado);

    UPDATE Exame
    SET status = 'R'
    WHERE id_exame = p_id_exame;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE SP_RealizarAltaPaciente(IN p_id_internacao INT, IN p_data_alta DATE)
BEGIN
    UPDATE Internacao
    SET data_alta_efetiva = p_data_alta
    WHERE id_internacao = p_id_internacao AND data_alta_efetiva IS NULL;
END$$

DELIMITER ;