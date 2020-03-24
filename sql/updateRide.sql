DROP PROCEDURE IF EXISTS updateRide;

DELIMITER //
CREATE PROCEDURE updateRide(IN ride_id_in INT, IN time_of_ride_in VARCHAR(50))
BEGIN
    UPDATE rideOffered
    SET departure_time=time_of_ride_in WHERE ride_id=ride_id_in;
    SELECT * FROM rideOffered WHERE ride_id=ride_id_in;
END//
DELIMITER ;
