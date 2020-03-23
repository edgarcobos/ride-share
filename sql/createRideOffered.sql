DROP TABLE IF EXISTS rideOffered;
CREATE TABLE rideOffered(
    ride_id INT NOT NULL AUTO_INCREMENT,
    from_location VARCHAR(50) NOT NULL,
    to_location VARCHAR(50) ,
    make_model VARCHAR(100),
    license_plate VARCHAR(50),
    driver_id VARCHAR(50) NOT NULL,
    departure_time VARCHAR(50) NOT NULL,
    PRIMARY KEY (ride_id),
    FOREIGN KEY (driver_id) REFERENCES users(user_id)
);
