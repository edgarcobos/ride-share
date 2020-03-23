DROP PROCEDURE IF EXISTS deleteRide;

DELIMITER //
CREATE PROCEDURE deleteRide(IN user_id_in INT, IN ride_id_in INT)
BEGIN
DELETE FROM rideOffered WHERE driver_id=user_id_in AND ride_id=ride_id_in;
END//
DELIMITER ;
