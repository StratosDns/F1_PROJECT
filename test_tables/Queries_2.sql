-- Find all measurements recorded by weather 
-- measurement kits installed in a grandprix 
-- of your choice

SELECT wk.kit_id, wk.location, m.*
FROM weather_kits wk
JOIN kit_measurements km ON wk.kit_id = km.kit_id,
LATERAL unnest(km.measurements) AS m
WHERE wk.raceid = 1;

-- Find the maximum temperature recorded by each 
-- weather measurement kit installed in a 
-- grandprix of your choice

SELECT wk.kit_id, wk.location,
       MAX((m).temp_celsius) AS max_temp
FROM weather_kits wk
JOIN kit_measurements km ON wk.kit_id = km.kit_id,
LATERAL unnest(km.measurements) AS m
WHERE wk.raceid = 1
GROUP BY wk.kit_id, wk.location;

-- Find the total number of measurements recorded 
-- by each weather measurement kit installed in a 
-- grandprix of your choice

SELECT wk.kit_id, wk.location,
       count(*) AS num_measurements
FROM weather_kits wk
JOIN kit_measurements km ON wk.kit_id = km.kit_id,
LATERAL unnest(km.measurements) AS m
WHERE wk.raceid = 1
GROUP BY wk.kit_id, wk.location;

-- Checking the total available data from kits
SELECT wk.*, km.measurements
FROM weather_kits wk
LEFT JOIN kit_measurements km ON wk.kit_id = km.kit_id
ORDER BY wk.raceid, wk.kit_id;