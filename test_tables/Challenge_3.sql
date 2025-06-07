DROP TABLE IF EXISTS event_sensor_measurement CASCADE;
DROP TABLE IF EXISTS periodic_sensor_measurement CASCADE;
DROP TABLE IF EXISTS continuous_sensor_measurement CASCADE;
DROP TABLE IF EXISTS sensor_measurement_base CASCADE;
DROP TYPE IF EXISTS sensor_unit CASCADE;
DROP TYPE IF EXISTS event_type CASCADE;


-- ===============================
-- 1. ENUMS and Supporting Types
-- ===============================

CREATE TYPE sensor_unit AS ENUM ('Celsius', 'bar', 'g-force', 'psi', 'event', 'percent');
CREATE TYPE event_type AS ENUM ('DRS', 'override', 'emergency_brake', 'pit_entry');

-- ===============================
-- 2. Sensor Measurement Hierarchy
-- ===============================
DROP TABLE IF EXISTS event_sensor_measurement CASCADE;
DROP TABLE IF EXISTS periodic_sensor_measurement CASCADE;
DROP TABLE IF EXISTS continuous_sensor_measurement CASCADE;
DROP TABLE IF EXISTS sensor_measurement_base CASCADE;

CREATE TABLE sensor_measurement_base (
    measurement_id SERIAL PRIMARY KEY,
    race_id INTEGER NOT NULL,
    lap INTEGER NOT NULL,
    car_id INTEGER NOT NULL,
    sensor_type TEXT NOT NULL,
    unit sensor_unit NOT NULL
);

-- (A) CONTINUOUS - Use JSONB for time-series (timestamp+value)
CREATE TABLE continuous_sensor_measurement (
    measurement_id INTEGER PRIMARY KEY,
    race_id INTEGER NOT NULL,
    lap INTEGER NOT NULL,
    car_id INTEGER NOT NULL,
    sensor_type TEXT NOT NULL,
    unit sensor_unit NOT NULL,
    time_series JSONB  -- [{"timestamp":..., "value":...}, ...]
) INHERITS (sensor_measurement_base);

-- (B) PERIODIC - Use arrays for values, plus interval info
CREATE TABLE periodic_sensor_measurement (
    measurement_id INTEGER PRIMARY KEY,
    race_id INTEGER NOT NULL,
    lap INTEGER NOT NULL,
    car_id INTEGER NOT NULL,
    sensor_type TEXT NOT NULL,
    unit sensor_unit NOT NULL,
    start_time TIMESTAMP NOT NULL,
    interval_seconds INTEGER NOT NULL,
    values NUMERIC[] NOT NULL
) INHERITS (sensor_measurement_base);

-- (C) EVENT-BASED - Use XML for event payload
CREATE TABLE event_sensor_measurement (
    measurement_id INTEGER PRIMARY KEY,
    race_id INTEGER NOT NULL,
    lap INTEGER NOT NULL,
    car_id INTEGER NOT NULL,
    sensor_type TEXT NOT NULL,
    unit sensor_unit NOT NULL,
    event_info XML NOT NULL
) INHERITS (sensor_measurement_base);

-- ======================================
-- 3. HOW TO INSERT: Continuous Example
-- ======================================

-- SENSOR 1: Engine Temperature (continuous)
INSERT INTO continuous_sensor_measurement (
    measurement_id, 
    race_id, lap, car_id, sensor_type, unit, time_series
) VALUES (
    DEFAULT, 1, 12, 44, 'engine_temperature', 'Celsius',
    '[{"timestamp":"2024-06-08T14:01:00","value":102.5},
      {"timestamp":"2024-06-08T14:01:01","value":102.6}]'
);

-- SENSOR 2: G-Force (continuous)
INSERT INTO continuous_sensor_measurement (
    measurement_id, race_id, lap, car_id, sensor_type, unit, time_series
) VALUES (
    DEFAULT, 1, 12, 44, 'g_force', 'g-force',
    '[{"timestamp":"2024-06-08T14:01:00","value":1.7},
      {"timestamp":"2024-06-08T14:01:01","value":1.9}]'
);

-- =====================================
-- 4. HOW TO INSERT: Periodic Example
-- =====================================

-- SENSOR 3: Tire Pressure (periodically)
INSERT INTO periodic_sensor_measurement (
    measurement_id, race_id, lap, car_id, sensor_type, unit, start_time, interval_seconds, values
) VALUES (
    DEFAULT, 1, 12, 44, 'tire_pressure', 'psi',
    '2024-06-08T14:01:00', 3, ARRAY[21.4, 21.2, 21.1, 21.3, 21.2]
);

-- SENSOR 4: Hydraulic Pressure (periodically)
INSERT INTO periodic_sensor_measurement (
    measurement_id, race_id, lap, car_id, sensor_type, unit, start_time, interval_seconds, values
) VALUES (
    DEFAULT, 1, 12, 44, 'hydraulic_pressure', 'bar',
    '2024-06-08T14:01:00', 3, ARRAY[88.1, 88.3, 88.2, 88.5, 88.7]
);

-- =====================================
-- 5. HOW TO INSERT: Event Example
-- =====================================

-- SENSOR 5: DRS Activation (event-based)
INSERT INTO event_sensor_measurement (
    measurement_id, race_id, lap, car_id, sensor_type, unit, event_info
) VALUES (
    DEFAULT, 1, 12, 44, 'drs_event', 'event',
    '<event>
     <type>DRS</type>
     <timestamp>2024-06-08T14:01:20</timestamp>
     <sector>3</sector>
     <triggered_by>driver</triggered_by>
   </event>'
);

-- SENSOR 6: Emergency Brake Activation (event-based)
INSERT INTO event_sensor_measurement (
    measurement_id, race_id, lap, car_id, sensor_type, unit, event_info
) VALUES (
    DEFAULT, 1, 12, 44, 'emergency_brake_event', 'event',
    '<event>
      <type>emergency_brake</type>
      <timestamp>2024-06-08T14:01:55</timestamp>
      <sector>1</sector>
      <triggered_by>driver</triggered_by>
    </event>'
);

-- more data insertion

-- CONTINUOUS SENSORS

-- Engine Temperature, Car 44, Lap 12 & Lap 13
INSERT INTO continuous_sensor_measurement (measurement_id, race_id, lap, car_id, sensor_type, unit, time_series)
VALUES
  (DEFAULT, 1, 12, 44, 'engine_temperature', 'Celsius',
   '[{"timestamp":"2024-06-08T14:01:00","value":102.5},{"timestamp":"2024-06-08T14:01:01","value":102.7},{"timestamp":"2024-06-08T14:01:02","value":102.9}]'),
  (DEFAULT, 1, 13, 44, 'engine_temperature', 'Celsius',
   '[{"timestamp":"2024-06-08T14:06:00","value":103.0},{"timestamp":"2024-06-08T14:06:01","value":103.1},{"timestamp":"2024-06-08T14:06:02","value":103.3}]'),

-- G-Force, Car 77, Lap 12
  (DEFAULT, 1, 12, 77, 'g_force', 'g-force',
   '[{"timestamp":"2024-06-08T14:01:00","value":1.8},{"timestamp":"2024-06-08T14:01:01","value":2.0},{"timestamp":"2024-06-08T14:01:02","value":1.9}]'),

-- Brake Disc Temperature, Car 44, Lap 13
  (DEFAULT, 1, 13, 44, 'brake_disc_temp', 'Celsius',
   '[{"timestamp":"2024-06-08T14:06:05","value":490.1},{"timestamp":"2024-06-08T14:06:06","value":492.5}]');

-- PERIODIC

-- Tire Pressure, Car 44, Lap 13
INSERT INTO periodic_sensor_measurement (measurement_id, race_id, lap, car_id, sensor_type, unit, start_time, interval_seconds, values)
VALUES
  (DEFAULT, 1, 13, 44, 'tire_pressure', 'psi', '2024-06-08T14:06:00', 3, ARRAY[21.2, 21.1, 21.2, 21.3, 21.2]),

-- Oil Pressure, Car 77, Lap 13
  (DEFAULT, 1, 13, 77, 'oil_pressure', 'bar', '2024-06-08T14:06:00', 4, ARRAY[7.7, 7.6, 7.8, 7.7, 7.9]);

-- EVENT-BASED

-- DRS Events, Car 44 and 77, different laps
INSERT INTO event_sensor_measurement (measurement_id, race_id, lap, car_id, sensor_type, unit, event_info)
VALUES
  (DEFAULT, 1, 12, 44, 'drs_event', 'event',
   '<event>
        <type>DRS</type>
        <timestamp>2024-06-08T14:01:24</timestamp>
        <sector>3</sector>
        <triggered_by>driver</triggered_by>
        </event>'
  ),
  (DEFAULT, 1, 13, 77, 'drs_event', 'event',
   '<event>
        <type>DRS</type>
        <timestamp>2024-06-08T14:06:35</timestamp>
        <sector>1</sector>
        <triggered_by>driver</triggered_by>
        </event>'
  );,

-- Pit Entry, Car 44, Lap 14
  (DEFAULT, 1, 14, 44, 'pit_entry', 'event',
   '<event>
        <type>pit_entry</type>
        <timestamp>2024-06-08T14:11:01</timestamp>
        <lane>main</lane>
        </event>'
  );