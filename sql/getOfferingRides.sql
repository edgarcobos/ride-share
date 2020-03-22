DELIMITER //
DROP PROCEDURE IF EXISTS getOfferingRides //

-- retrieves all offering rides
CREATE PROCEDURE getOfferingRides()
BEGIN
  SELECT * FROM rides WHERE taken=0 AND passenger_user IS NULL;
END //
DELIMITER ;

DELIMITER //
DROP PROCEDURE IF EXISTS getOfferingDriverRides //

-- retrieves offering rides by driver
CREATE PROCEDURE getOfferingDriverRides(IN user_id_in VARCHAR(50))
BEGIN
  SELECT * FROM rides WHERE driver_user=user_id_in AND taken=0 AND passenger_user IS NULL;
END //
DELIMITER ;
