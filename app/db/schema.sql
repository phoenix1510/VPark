CREATE DATABASE IF NOT EXISTS parking_db;
USE parking_db;

CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone_number VARCHAR(50) NOT NULL,
    role ENUM('user', 'admin') NOT NULL DEFAULT 'user'
);

CREATE TABLE facility (
    facility_id INT PRIMARY KEY AUTO_INCREMENT,
    facility_name VARCHAR(100) NOT NULL,
    user_id INT,
    address TEXT NOT NULL,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE SET NULL
);

CREATE TABLE floor (
    floor_id INT PRIMARY KEY AUTO_INCREMENT,
    floor_number INT NOT NULL,
    facility_id INT,

    FOREIGN KEY (facility_id)
        REFERENCES facility(facility_id)
        ON DELETE CASCADE,

    UNIQUE (facility_id, floor_number)
);

CREATE TABLE parking_slot (
    slot_id INT PRIMARY KEY AUTO_INCREMENT,
    slot_number INT NOT NULL,
    status ENUM('occupied', 'vacant', 'unavailable') DEFAULT 'vacant',
    floor_id INT,

    FOREIGN KEY (floor_id)
        REFERENCES floor(floor_id)
        ON DELETE CASCADE,

    UNIQUE (floor_id, slot_number)
);

CREATE TABLE parking_rate (
    rate_id INT PRIMARY KEY AUTO_INCREMENT,
    vehicle_type VARCHAR(50),
    rate_per_hour INT NOT NULL,
    facility_id INT,

    FOREIGN KEY (facility_id)
        REFERENCES facility(facility_id)
        ON DELETE CASCADE
);

CREATE TABLE vehicle (
    vehicle_id INT PRIMARY KEY AUTO_INCREMENT,
    vehicle_name VARCHAR(50) NOT NULL,
    registration_number VARCHAR(255) NOT NULL UNIQUE,
    user_id INT,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE SET NULL
);

CREATE TABLE parking_session (
    session_id INT PRIMARY KEY AUTO_INCREMENT,
    entry_time DATETIME NOT NULL,
    exit_time DATETIME,
    status ENUM('active', 'completed', 'cancelled') NOT NULL DEFAULT 'active',
    rate_id INT,
    rate_per_hour_used INT NOT NULL,
    vehicle_id INT,
    slot_id INT,

    FOREIGN KEY (vehicle_id)
        REFERENCES vehicle(vehicle_id)
        ON DELETE CASCADE,

    FOREIGN KEY (slot_id)
        REFERENCES parking_slot(slot_id)
        ON DELETE CASCADE,

    FOREIGN KEY (rate_id)
        REFERENCES parking_rate(rate_id)
        ON DELETE SET NULL
);