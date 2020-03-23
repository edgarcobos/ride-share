DROP PROCEDURE IF EXISTS takeRide;

DELIMITER //
-- this will be executed when a user confirms he/she took the ride
CREATE PROCEDURE takeRide(IN rideID_in INT, IN driverID_in VARCHAR(50), IN riderID_in VARCHAR(50))
BEGIN
INSERT INTO rideTaken VALUES(NULL, rideID_in, driverID_in, riderID_in);
SELECT * FROM rideTaken WHERE ride_id = rideID_in and rider_id = riderID_in;
END//
DELIMITER ;
