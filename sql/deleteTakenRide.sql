DROP PROCEDURE IF EXISTS deleteTakenRide;

DELIMITER //
CREATE PROCEDURE deleteTakenRide(IN user_id_in INT, IN ride_id_in INT)
BEGIN
DELETE FROM rideTaken WHERE rider_id=user_id_in AND ride_id=ride_id_in;
END//
DELIMITER ;