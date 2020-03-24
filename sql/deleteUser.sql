DROP PROCEDURE IF EXISTS deleteUser;

DELIMITER //
CREATE PROCEDURE deleteUser(IN user_id_in VARCHAR(50))
BEGIN
DELETE FROM rideOffered WHERE driver_id=user_id_in;
DELETE FROM rideTaken WHERE driver_id=user_id_in or rider_id=user_id_in;
DELETE FROM users WHERE user_id=user_id_in;
END//
DELIMITER ;