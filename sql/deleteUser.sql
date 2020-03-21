DROP PROCEDURE IF EXISTS deleteUser;

DELIMITER //
CREATE PROCEDURE deleteUser(IN user_id_in INT)
BEGIN
DELETE FROM rides WHERE driver_user=user_id_in;
DELETE FROM users WHERE user_id=user_id_in;
END//
DELIMITER ;