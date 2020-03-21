DELIMITER //
DROP PROCEDURE IF EXISTS getTakenRides //

CREATE PROCEDURE getTakenRides(IN user_id_in VARCHAR(50))
BEGIN
  SELECT * FROM rides WHERE passenger_user=user_id_in;
END //
DELIMITER ;
