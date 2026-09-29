-- MySQL setup for the bank project
-- The program can also create these automatically.

CREATE DATABASE IF NOT EXISTS bank;
USE bank;

CREATE TABLE IF NOT EXISTS customer (
    customer_id INT PRIMARY KEY,
    name VARCHAR(30),
    YOB VARCHAR(5),
    IFSC VARCHAR(15),
    phone_number INT
);
