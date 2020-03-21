DROP PROCEDURE IF EXISTS getRideById;

DELIMITER //
CREATE PROCEDURE getRideById(IN user_id_in VARCHAR(50), IN ride_id_in INT)
BEGIN
SELECT * FROM rides WHERE driver_user=user_id_in AND ride_id=ride_id_in;
END//
DELIMITER ;
