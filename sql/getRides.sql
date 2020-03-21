DELIMITER //
DROP PROCEDURE IF EXISTS getTakenRides //

CREATE PROCEDURE getPassengerRides(IN user_id_in VARCHAR(50))
BEGIN
  SELECT * FROM rides WHERE passenger_user=user_id_in;
END //
DELIMITER ;

DELIMITER //
DROP PROCEDURE IF EXISTS getOfferedRides //

CREATE PROCEDURE getDriverRides(IN user_id_in VARCHAR(50))
BEGIN
  SELECT * FROM rides WHERE driver_user=user_id_in;
END //
DELIMITER ;
