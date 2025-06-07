DROP TABLE IF EXISTS kit_measurements CASCADE;
DROP TABLE IF EXISTS weather_kits CASCADE;
DROP TYPE IF EXISTS weather_measurement CASCADE;
DROP TYPE IF EXISTS kit_location CASCADE;
DROP TYPE IF EXISTS weather_desc CASCADE;

-- (A) ENUM Types for Measurement Variable and Location

-- Enum for weather kit locations (define locations as appropriate)
CREATE TYPE kit_location AS ENUM ('start_finish', 'turn_1', 'back_straight');

-- Optional: Enum for weather descriptions
CREATE TYPE weather_desc AS ENUM ('sunny', 'cloudy', 'overcast', 'mostly sunny', 'rainy');


-- (B) Composite Type for Measurement Row

CREATE TYPE weather_measurement AS (
    measured_at TIMESTAMP,
    temp_celsius NUMERIC,
    precipitation_percent NUMERIC,
    humidity_percent NUMERIC,
    wind_kph NUMERIC,
    description weather_desc -- or TEXT if more flexibility is needed
);


-- (C) Weather Kits Table

CREATE TABLE weather_kits (
    kit_id SERIAL PRIMARY KEY,
    raceid INTEGER NOT NULL REFERENCES races(raceId),
    location kit_location NOT NULL
);


-- (D) Weather Measurements Table

-- Array of Composite Type per kit
CREATE TABLE kit_measurements (
    kit_id INTEGER REFERENCES weather_kits(kit_id),
    measurements weather_measurement[],
    PRIMARY KEY (kit_id)
);



-- Inserting Example Data

-- 1. Insert 3 weather kits for race 1
INSERT INTO weather_kits (raceid, location) VALUES
  (1, 'start_finish'),
  (1, 'turn_1'),
  (1, 'back_straight');

-- 2. Insert measurements for those kits (assuming their kit_ids are 1, 2, 3)
INSERT INTO kit_measurements (kit_id, measurements) VALUES
(1, ARRAY[
    ROW('2024-06-05 10:00', 13,   0, 44, 37, 'mostly sunny')::weather_measurement,
    ROW('2024-06-05 10:05', 13.4, 0, 44, 38, 'mostly sunny')::weather_measurement,
    ROW('2024-06-05 10:10', 14,   0, 43, 39, 'sunny')::weather_measurement
]);

INSERT INTO kit_measurements (kit_id, measurements) VALUES
(2, ARRAY[
    ROW('2024-06-05 10:00', 13.1, 0, 42, 35, 'mostly sunny')::weather_measurement,
    ROW('2024-06-05 10:05', 13.6, 0, 43, 36, 'mostly sunny')::weather_measurement,
    ROW('2024-06-05 10:10', 13.9, 0, 41, 36, 'sunny')::weather_measurement
]);

INSERT INTO kit_measurements (kit_id, measurements) VALUES
(3, ARRAY[
    ROW('2024-06-05 10:00', 12.8, 0, 45, 34, 'cloudy')::weather_measurement,
    ROW('2024-06-05 10:05', 13.0, 1, 47, 35, 'cloudy')::weather_measurement,
    ROW('2024-06-05 10:10', 13.2, 1, 46, 35, 'mostly sunny')::weather_measurement
]);

-- 3. Insert 3 weather kits for race 2
INSERT INTO weather_kits (raceid, location) VALUES
  (2, 'start_finish'),
  (2, 'turn_1'),
  (2, 'back_straight');

-- 4. Find actual kit_ids for race 2 just added
-- SELECT * FROM weather_kits WHERE raceid = 2;
-- Suppose these kit_ids are 4, 5, 6.

-- 5. Insert measurements for those kits for race 2
INSERT INTO kit_measurements (kit_id, measurements) VALUES
(4, ARRAY[
    ROW('2024-06-06 10:00', 18.3, 0, 38, 30, 'sunny')::weather_measurement,
    ROW('2024-06-06 10:05', 18.9, 0, 39, 31, 'sunny')::weather_measurement
]);

INSERT INTO kit_measurements (kit_id, measurements) VALUES
(5, ARRAY[
    ROW('2024-06-06 10:00', 17.9, 0, 37, 32, 'overcast')::weather_measurement,
    ROW('2024-06-06 10:05', 18.2, 0, 39, 33, 'cloudy')::weather_measurement
]);

INSERT INTO kit_measurements (kit_id, measurements) VALUES
(6, ARRAY[
    ROW('2024-06-06 10:00', 18.5, 0, 38, 31, 'sunny')::weather_measurement
]);



