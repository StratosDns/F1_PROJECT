-- Get all temperature sensor data
SELECT * FROM continuous_sensor_measurement WHERE sensor_type = 'engine_temperature';

-- Get all event measurements
SELECT * FROM event_sensor_measurement;

--  Find max engine temperature for each lap of car 44

SELECT
  csm.lap,
  MAX((v.elem->>'value')::NUMERIC) AS max_temp
FROM continuous_sensor_measurement csm
CROSS JOIN LATERAL jsonb_array_elements(csm.time_series) AS v(elem)
WHERE csm.car_id = 44 AND csm.sensor_type = 'engine_temperature'
GROUP BY csm.lap
ORDER BY csm.lap;

-- List all tire pressure readings in timestamped format for car 44, lap 13

SELECT
  start_time + (i-1) * interval_seconds * INTERVAL '1 SECOND' AS reading_time,
  values[i] AS psi_value
FROM periodic_sensor_measurement,
LATERAL generate_subscripts(values, 1) AS g(i)
WHERE car_id = 44 AND lap = 13 AND sensor_type = 'tire_pressure'
ORDER BY reading_time;

-- Count number of DRS activations by lap for each car

SELECT car_id, lap, COUNT(*) AS drs_activations
FROM event_sensor_measurement
WHERE sensor_type = 'drs_event'
GROUP BY car_id, lap
ORDER BY car_id, lap;

-- Find all peak g-force values recorded (any car, any lap)

SELECT
  csm.car_id, csm.lap,
  MAX((v.elem->>'value')::NUMERIC) as peak_gforce
FROM continuous_sensor_measurement csm
CROSS JOIN LATERAL jsonb_array_elements(csm.time_series) AS v(elem)
WHERE csm.sensor_type = 'g_force'
GROUP BY csm.car_id, csm.lap
ORDER BY peak_gforce DESC;

-- Get all event-based activations for car 44: type, timestamp, lap

SELECT
  lap, 
  (xpath('/event/type/text()', event_info))[1]::TEXT as event_type,
  (xpath('/event/timestamp/text()', event_info))[1]::TEXT as event_time
FROM event_sensor_measurement
WHERE car_id = 44
ORDER BY lap, event_time;

-- Average oil pressure for car 77 over all periodic measurements

SELECT
  AVG(avg_val) as avg_oil_pressure
FROM (
  SELECT car_id, AVG(val) as avg_val
  FROM periodic_sensor_measurement,
       LATERAL unnest(values) AS u(val)
  WHERE sensor_type = 'oil_pressure' AND car_id = 77
  GROUP BY measurement_id, car_id
) sub;

-- For each car, lap, list ALL sensor types recorded and their measurement method

SELECT
  s.car_id, s.lap, s.sensor_type,
  CASE
    WHEN s.sensor_type IN ('engine_temperature','g_force','brake_disc_temp') THEN 'continuous'
    WHEN s.sensor_type IN ('tire_pressure','oil_pressure') THEN 'periodic'
    WHEN s.sensor_type IN ('drs_event','pit_entry') THEN 'event'
    ELSE 'unknown'
  END AS measurement_category
FROM sensor_measurement_base s
ORDER BY s.car_id, s.lap, measurement_category;

