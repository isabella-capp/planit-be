CREATE DATABASE IF NOT EXISTS test_db;
CREATE DATABASE IF NOT EXISTS mysql_db;

USE mysql_db;

DROP TABLE IF EXISTS events;
CREATE TABLE events (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,         -- Event's name
  start_time TIME NULL,               -- Start time
  end_time TIME NULL,                 -- End time
  dates TEXT NOT NULL                 -- Selected dates, stored as a list 
);

DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,     -- Unique identifier for each user
  username VARCHAR(255) UNIQUE,          -- User's username
  email VARCHAR(255) UNIQUE,             -- User's email (must be unique)
  password_hash VARCHAR(255)             -- Hashed password for security
);


INSERT INTO users (username, email, password_hash) VALUES
  ('admin', 'admin@gmail.com', 'root'),
  ('isa_cap', 'isa.cappellino@gmail.com', 'cappellino');

INSERT INTO events (name, start_time, end_time, dates) VALUES
  ('Event 1', '10:00:00', '12:00:00', '2021-10-01, 2021-10-02, 2021-10-03'),
  ('Event 2', '14:00:00', '16:00:00', '2021-10-01, 2021-10-02, 2021-10-03'),
  ('Event 3', '18:00:00', '20:00:00', '2021-10-01, 2021-10-02, 2021-10-03');


