import pandas as pd
import random
import json
from datetime import datetime, timedelta

# Load data
results = pd.read_csv('C:/F1_Project/data/postgres/results.csv')
lap_times = pd.read_csv('C:/F1_Project/data/postgres/lap_times.csv')
pit_stops = pd.read_csv('C:/F1_Project/data/postgres/pit_stops.csv')
status = pd.read_csv('C:/F1_Project/data/postgres/status.csv')

# Build valid (raceId, driverId) pairs
valid_pairs = results[['raceId', 'driverId']].drop_duplicates().values.tolist()

# Map each (raceId, driverId) to valid laps
lap_map = lap_times.groupby(['raceId', 'driverId'])['lap'].unique().to_dict()

# Build pit stop lookup: (raceId, driverId) -> set of pit stop laps
pit_lap_map = pit_stops.groupby(['raceId', 'driverId'])['lap'].unique().to_dict()

# Build engine failure lookup: (raceId, driverId) where status is 'Engine'
engine_status_ids = status[status['status'].str.lower().str.contains('engine')]['statusId'].astype(str).tolist()
engine_failures = set(
    tuple(x) for x in results[results['statusId'].astype(str).isin(engine_status_ids)][['raceId', 'driverId']].values
)

mechanic_names = [
    "John Smith", "Lisa Turner", "Mike Brown", "Sara White", "Alex Green", "Chris Black",
    "Emily Adams", "Jacob Evans", "Olivia Scott", "Daniel Lee", "Grace Clark", "Ryan Hall",
    "Sophie King", "Luke Walker", "Emma Young", "Benjamin Allen", "Ella Martin",
    "Mason Wright", "Chloe Harris", "Nathan Lewis"
]

# Message templates: (text, type, tags, [special_condition])
message_templates = [
    ("Box this lap for softs.", "strategy", ["pitstop", "softs", "first_stop"], "pit_now"),
    ("Box now for mediums.", "strategy", ["pitstop", "mediums", "first_stop"], "pit_now"),
    ("Box for hards.", "strategy", ["pitstop", "hards", "first_stop"], "pit_now"),
    ("Box next lap for inters.", "strategy", ["pitstop", "inters", "weather"], "pit_next"),
    ("Box next lap for softs.", "strategy", ["pitstop", "softs", "next"], "pit_next"),
    ("Engine overheating, reduce power.", "engine", ["engine", "overheating"], "engine_fail"),
    ("Retire the car, loss of power.", "retirement", ["retirement", "engine"], "engine_fail"),
    # -- General messages (no special condition) --
    ("Save fuel, engine mode 5.", "engine", ["engine", "fuel_saving"], None),
    ("Yellow flag in sector 2.", "alert", ["yellow_flag", "sector2"], None),
    ("Rain expected in 10 minutes.", "weather", ["weather", "rain"], None),
    ("Switch to engine mode 7.", "engine", ["engine", "mode_change"], None),
    ("DRS enabled.", "info", ["drs", "info"], None),
    ("Red flag, enter the pit lane.", "alert", ["red_flag", "alert"], None),
    ("Prepare for safety car restart.", "alert", ["safety_car", "restart"], None),
    ("Front wing damage, box for repairs.", "alert", ["damage", "pitstop", "repair"], None),
    ("Hold position, conserve tyres.", "strategy", ["tyre_management", "conserve"], None),
    ("Pit lane speeding, 5 sec penalty.", "penalty", ["penalty", "pitlane_speeding"], None),
    ("Switch to wets, rain intensifying.", "weather", ["pitstop", "wets", "weather"], None),
    ("Harvest energy, charge battery.", "engine", ["harvest", "battery"], None),
    ("Virtual safety car deployed.", "alert", ["vsc", "alert"], None),
    ("Box for softs, push now.", "strategy", ["pitstop", "softs"], None),
    ("Check tyre temps, tyres are cold.", "info", ["tyre_management", "cold"], None),
    ("Increase brake bias forward.", "engine", ["brakes", "bias"], None),
    ("Blue flags, let car behind through.", "alert", ["blue_flag", "alert"], None),
    ("Pit for softs, final stint.", "strategy", ["pitstop", "softs", "final_stint"], None),
    ("Pit for mediums, car behind boxing.", "strategy", ["pitstop", "mediums", "gap"], None),
    ("Brake temps high, adjust pace.", "engine", ["brakes", "high_temp"], None),
    ("Good job, currently P3.", "info", ["position", "info"], None),
    ("Pit for hards, tyres at limit.", "strategy", ["pitstop", "hards", "tyre_degradation"], None),
    ("Final lap, bring it home.", "info", ["final_lap", "info"], None)
]

start_time = datetime(2025, 6, 7, 13, 0, 0)
messages = []
message_count = 5000  # or whatever you want

for i in range(message_count):
    race_id, driver_id = random.choice(valid_pairs)
    laps = lap_map.get((race_id, driver_id), list(range(1, 56)))
    lap = int(random.choice(laps))
    mechanic = random.choice(mechanic_names)

    # Find which templates are allowed on this lap
    allowed_templates = []
    for tpl in message_templates:
        text, typ, tags, condition = tpl
        pit_laps = set(pit_lap_map.get((race_id, driver_id), []))
        if condition == "pit_now":
            if lap in pit_laps:
                allowed_templates.append(tpl)
        elif condition == "pit_next":
            if (lap+1) in pit_laps:
                allowed_templates.append(tpl)
        elif condition == "engine_fail":
            if (race_id, driver_id) in engine_failures:
                allowed_templates.append(tpl)
        elif condition is None:
            allowed_templates.append(tpl)

    if not allowed_templates:
        continue  # skip this message if nothing valid to say

    template = random.choice(allowed_templates)
    timestamp = start_time + timedelta(minutes=2*i)
    messages.append({
        "message_id": f"msg{str(len(messages)+1).zfill(3)}",
        "race_id": int(race_id),
        "driver_id": int(driver_id),
        "mechanic_name": mechanic,
        "timestamp": timestamp.isoformat() + "Z",
        "lap": lap,
        "message_text": template[0],
        "message_type": template[1],
        "tags": template[2]
    })

with open("C:/F1_Project/data/mongo/data_mongo_driver_radio_messages.json", "w") as f:
    json.dump(messages, f, indent=2)

print("Realistic synthetic radio messages generated!")