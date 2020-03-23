DELIMITER //
DROP PROCEDURE IF EXISTS getOfferedRides //

CREATE PROCEDURE getOfferedRides()
BEGIN
  SELECT * FROM rideOffered;
END //
DELIMITER ;

DELIMITER //
DROP PROCEDURE IF EXISTS getOfferedRidesByUser //

CREATE PROCEDURE getOfferedRidesByUser(IN driver_id_in VARCHAR(50))
BEGIN
  SELECT * FROM rideOffered WHERE driver_id=driver_id_in;
END //
DELIMITER ;

DELIMITER //
DROP PROCEDURE IF EXISTS getOfferedRidesByID //

CREATE PROCEDURE getOfferedRidesByID(IN ride_id_in INT)
BEGIN
  SELECT * FROM rideOffered WHERE ride_id=ride_id_in;
END //
DELIMITER ;

DELIMITER //
DROP PROCEDURE IF EXISTS getOfferedRidesByIDAndDriver //

CREATE PROCEDURE getOfferedRidesByIDAndDriver(IN ride_id_in INT, IN driver_id_in VARCHAR(50))
BEGIN
  SELECT * FROM rideOffered WHERE ride_id=ride_id_in AND driver_id=driver_id_in;
END //
DELIMITER ;
