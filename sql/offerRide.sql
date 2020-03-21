DROP PROCEDURE IF EXISTS offerRide;

DELIMITER //
CREATE PROCEDURE offerRide(IN time_of_ride_in VARCHAR(50), IN to_location_in VARCHAR(50), IN from_location_in VARCHAR(50), IN passenger_user_in VARCHAR(50))
BEGIN
    INSERT INTO rides(time_of_ride, to_location, from_location, driver_user) VALUES (time_of_ride_in, to_location_in, from_location_in, passenger_user_in);
    SELECT * FROM rides ORDER BY ride_id DESC LIMIT 1;
END//
DELIMITER ;

-- call requestRide('Fri Feb 21 at 7:30', '580 Montgomery St', 'Lunar Rogue Pub', 'ssanchez');
