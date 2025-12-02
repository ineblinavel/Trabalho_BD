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

CREATE TRIGGER TRG_SyncMedicoUsuario_Ativo
AFTER UPDATE ON Medicos
FOR EACH ROW
BEGIN
    IF OLD.ativo IS NOT NULL AND NEW.ativo IS NOT NULL AND OLD.ativo <> NEW.ativo THEN
        UPDATE Usuarios
        SET ativo = NEW.ativo
        WHERE referencia_id = NEW.crm AND role = 'medico';
    END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER TRG_DeleteEnfermeiro_DeleteUsuario
AFTER DELETE ON Enfermeiro
FOR EACH ROW
BEGIN
    DELETE FROM Usuarios WHERE referencia_id = OLD.corem AND role = 'enfermeiro';
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
