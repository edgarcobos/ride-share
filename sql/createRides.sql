DROP TABLE IF EXISTS rides;
CREATE TABLE rides(
    ride_id INT AUTO_INCREMENT,
    time_of_ride VARCHAR(50) NOT NULL,
    to_location VARCHAR(50) NOT NULL,
    from_location VARCHAR(50) NOT NULL,
    car_model VARCHAR(50),
    license_plate VARCHAR(50),
    passenger_user VARCHAR(50),
    driver_user VARCHAR(50) NOT NULL,
    price DECIMAL(50),
    taken BOOLEAN DEFAULT 0,
    PRIMARY KEY (ride_id),
    FOREIGN KEY (passenger_user) REFERENCES Users(user_id),
    FOREIGN KEY (driver_user) REFERENCES Users(user_id)
);
