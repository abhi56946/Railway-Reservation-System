
CREATE DATABASE IF NOT EXISTS railway_reservation;

USE railway_reservation;

CREATE TABLE IF NOT EXISTS trains (
    train_no INT PRIMARY KEY,
    train_name VARCHAR(100) NOT NULL,
    source VARCHAR(50) NOT NULL,
    destination VARCHAR(50) NOT NULL,
    total_seats INT NOT NULL,
    available_seats INT NOT NULL
);
