DELIMITER $$

CREATE TRIGGER TRG_ValidarAltaInternacao
BEFORE UPDATE ON Internacao
FOR EACH ROW
BEGIN
    IF NEW.data_alta_efetiva IS NOT NULL AND NEW.data_alta_efetiva < NEW.data_admissao THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erro: A data de alta não pode ser anterior à data de admissão.';
    END IF;
END$$

DELIMITER ;


DELIMITER $$

CREATE TRIGGER TRG_AuditoriaSalario
AFTER UPDATE ON Medicos
FOR EACH ROW
BEGIN
    IF OLD.salario <> NEW.salario THEN
        INSERT INTO LogSalario (crm_medico, salario_antigo, salario_novo, data_alteracao)
        VALUES (OLD.crm, OLD.salario, NEW.salario, NOW());
    END IF;
END$$

DELIMITER ;
