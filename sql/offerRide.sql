DROP PROCEDURE IF EXISTS offerRide;

DELIMITER //
-- this will be executed when a user offers a ride that has been requested
CREATE PROCEDURE offerRide(IN from_in VARCHAR(50), IN to_in VARCHAR(50), IN makeModel_in VARCHAR(100), IN licensePlate_in VARCHAR(50),
	IN driverID_in VARCHAR(50), IN time_in VARCHAR(50))
BEGIN
INSERT INTO rideOffered VALUES(NULL, from_in, to_in, makeModel_in, licensePlate_in, driverID_in, time_in);
SELECT * FROM rideOffered ORDER BY ride_id DESC LIMIT 1;
END//
DELIMITER ;
