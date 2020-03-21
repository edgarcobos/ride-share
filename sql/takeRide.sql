DROP PROCEDURE IF EXISTS takeRide;

DELIMITER //
-- this will be executed when a user confirms he/she took the ride
CREATE PROCEDURE takeRide(IN ride_id_in INT, IN user_id_in VARCHAR(50))
BEGIN
UPDATE rides
    SET passenger_user=user_id_in AND taken=1
    WHERE ride_id=ride_id_in;
    SELECT * FROM rides WHERE ride_id=ride_id_in;
END//
DELIMITER ;
