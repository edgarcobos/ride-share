DELIMITER //
DROP PROCEDURE IF EXISTS getTakenRides //

CREATE PROCEDURE getTakenRides(IN user_id_in VARCHAR(50))
BEGIN
  SELECT * FROM rideTaken WHERE rider_id=user_id_in;
END //
DELIMITER ;

DELIMITER //
DROP PROCEDURE IF EXISTS getTakenRidesByID //

CREATE PROCEDURE getTakenRidesByID(IN user_id_in VARCHAR(50), IN ride_id_in INT)
BEGIN
  SELECT * FROM rideTaken WHERE rider_id=user_id_in AND ride_id=ride_id_in;
END //
DELIMITER ;
