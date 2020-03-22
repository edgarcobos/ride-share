DROP PROCEDURE IF EXISTS updateRide;

DELIMITER //
CREATE PROCEDURE updateRide(IN ride_id_in INT, IN time_of_ride_in VARCHAR(50), IN price_in INT, IN driver_user_in VARCHAR(50))
BEGIN
    UPDATE rides
    SET time_of_ride=time_of_ride_in,
    	price=price_in
    WHERE ride_id=ride_id_in;
    SELECT * FROM rides WHERE ride_id=ride_id_in;
END//
DELIMITER ;
