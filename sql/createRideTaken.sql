DROP TABLE IF EXISTS rideTaken;
CREATE TABLE rideTaken(
    useless_id INT NOT NULL AUTO_INCREMENT,
    ride_id INT NOT NULL,
    driver_id VARCHAR(50) NOT NULL,
    rider_id VARCHAR (50) NOT NULL,
    PRIMARY KEY (useless_id),
    FOREIGN KEY (ride_id) REFERENCES rideOffered(ride_id),
    FOREIGN KEY (driver_id) REFERENCES users(user_id),
    FOREIGN KEY (rider_id) REFERENCES users(user_id)
);