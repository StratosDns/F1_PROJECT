DROP TABLE IF EXISTS grandprix_lineups CASCADE;
DROP TABLE IF EXISTS races CASCADE;
DROP TABLE IF EXISTS drivers CASCADE;

-- Grand Prix table
CREATE TABLE races (
    raceId INTEGER NOT NULL,
    year INTEGER,
    round TEXT,
    circuitId INTEGER ,
    name TEXT ,
    date TEXT,
    time TEXT,
    url TEXT,
    fp1_date TEXT,
    fp1_time TEXT,
    fp2_date TEXT,
    fp2_time TEXT,
    fp3_date TEXT,
    fp3_time TEXT,
    quali_date TEXT,
    quali_time TEXT,
    sprint_date TEXT,
    sprint_time TEXT,
    PRIMARY KEY (raceId)
);

-- Drivers
CREATE TABLE drivers (
    driverId INTEGER NOT NULL,
    driverRef TEXT,
    number  TEXT,
    code TEXT,
    forename TEXT,
    surname TEXT,
    dob TEXT,
    nationality TEXT,
    url TEXT,
    PRIMARY KEY (driverId)
);

CREATE TABLE results (
    resultId       INTEGER NOT NULL,
    raceId         INTEGER NOT NULL,
    driverId       INTEGER NOT NULL,
    constructorId  INTEGER NOT NULL,         
    number         TEXT,         
    grid           TEXT,         
    position       TEXT,         
    positionText   TEXT,        
    positionOrder  TEXT,         
    points         TEXT,         
    laps           TEXT,         
    time           TEXT,            
    milliseconds   TEXT,         
    fastestLap     TEXT,            
    rank           TEXT,       
    fastestLapTime TEXT,   
    fastestLapSpeed TEXT,      
    statusid       TEXT,         
    PRIMARY KEY (resultId),
    FOREIGN KEY (raceId) REFERENCES races(raceId),
    FOREIGN KEY (driverId) REFERENCES drivers(driverId)
);

COPY races FROM 'C:\uni\8x\ATD\archive\races.csv' DELIMITER ',' CSV HEADER;

COPY drivers FROM 'C:\uni\8x\ATD\archive\drivers.csv' DELIMITER ',' CSV HEADER;

COPY results FROM 'C:\uni\8x\ATD\archive\results.csv' DELIMITER ',' CSV HEADER;

CREATE TABLE grandprix_lineups (
    raceId INTEGER PRIMARY KEY REFERENCES races(raceId),
    lineup INTEGER[]  -- array of driver_id, order = starting grid position
);

-- Correct INSERT FOR LINEUPS
INSERT INTO grandprix_lineups (raceId, lineup)
SELECT
    raceId::INTEGER,
    array_agg(driverId::INTEGER ORDER BY grid::INTEGER) AS lineup
FROM results
WHERE grid <> '\N'
GROUP BY raceId
ON CONFLICT (raceId) DO NOTHING;

SELECT * FROM grandprix_lineups;