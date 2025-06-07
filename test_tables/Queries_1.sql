-- Query 1
/*
Find the drivers who started the race behind
the driver with a code of your choice in the
grandprix of your choice
*/

WITH
lineup_info AS (
    SELECT lineup
    FROM grandprix_lineups
    WHERE raceId = 2  -- Set your chosen raceId
),
target_pos AS (
    SELECT array_position(l.lineup, d.driverId) AS pos
    FROM drivers d
    CROSS JOIN lineup_info l
    WHERE d.driverId = 22       -- Set your chosen driverId here
)
SELECT dr.*
FROM lineup_info l
CROSS JOIN target_pos pos
CROSS JOIN LATERAL unnest(l.lineup) WITH ORDINALITY AS u(driverId, idx)
JOIN drivers dr ON dr.driverId = u.driverId
WHERE u.idx > pos.pos
ORDER BY u.idx;

-- Query 2
/*
Find the driver who started the race one 
position behind the driver with a code of
your choice in the grandprix of your choice
*/

WITH
  lineup_info AS (
    SELECT lineup
    FROM grandprix_lineups
    WHERE raceid = 2  -- Set your chosen raceId
  ),
  target_pos AS (
    SELECT array_position(l.lineup, d.driverid) AS pos
    FROM drivers d
    CROSS JOIN lineup_info l
    WHERE d.driverid = 22   -- Set your chosen driverId
  )
SELECT dr.*
FROM lineup_info l
CROSS JOIN target_pos pos
CROSS JOIN LATERAL unnest(l.lineup) WITH ORDINALITY AS u(driverid, idx)
JOIN drivers dr ON dr.driverid = u.driverid
WHERE u.idx = pos.pos + 1;

-- Query 3
/*
Find the driver who started the race two
positions behind the driver with a code
of your choice in the grandprix of your 
choice
*/

WITH
  lineup_info AS (
    SELECT lineup
    FROM grandprix_lineups
    WHERE raceid = 2
  ),
  target_pos AS (
    SELECT array_position(l.lineup, d.driverid) AS pos
    FROM drivers d
    CROSS JOIN lineup_info l
    WHERE d.driverid = 22
  )
SELECT dr.*
FROM lineup_info l
CROSS JOIN target_pos pos
CROSS JOIN LATERAL unnest(l.lineup) WITH ORDINALITY AS u(driverid, idx)
JOIN drivers dr ON dr.driverid = u.driverid
WHERE u.idx = pos.pos + 2;

-- Query 4
/*
Find the driver who started the race in the
up front position in the grandprix of your choice
*/

WITH
  lineup_info AS (
    SELECT lineup
    FROM grandprix_lineups
    WHERE raceid = 2  -- Set your chosen raceId
  )
SELECT dr.*
FROM lineup_info l
CROSS JOIN LATERAL unnest(l.lineup) WITH ORDINALITY AS u(driverid, idx)
JOIN drivers dr ON dr.driverid = u.driverid
WHERE u.idx = 1;  -- Set your chosen position here