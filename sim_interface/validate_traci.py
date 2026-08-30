import os

import traci

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SUMOCFG_PATH = os.path.join(SCRIPT_DIR, "..", "sim.sumocfg")

NUM_STEPS = 50

traci.start(["sumo", "-c", SUMOCFG_PATH])

for step in range(1, NUM_STEPS + 1):
    traci.simulationStep()

print(f"\n{'=' * 60}")
print(f"INSPECTION AT STEP {NUM_STEPS}")
print(f"{'=' * 60}")

vehicle_ids = traci.vehicle.getIDList()
tls_ids = traci.trafficlight.getIDList()

veh_id = vehicle_ids[0]
x, y = traci.vehicle.getPosition(veh_id)
speed = traci.vehicle.getSpeed(veh_id)
road_id = traci.vehicle.getRoadID(veh_id)
lane_id = traci.vehicle.getLaneID(veh_id)
route = traci.vehicle.getRoute(veh_id)

print(f"\n--- Vehicle: {veh_id} ---")
print(f"Position:      ({x:.2f}, {y:.2f})")
print(f"Speed:         {speed:.2f} m/s")
print(f"Current edge:  {road_id}")
print(f"Current lane:  {lane_id}")
print(f"Route (edges): {route}")

# Lane the inspected vehicle is currently on, so the vehicle and lane
# numbers can be cross-checked against each other.
queue = traci.lane.getLastStepHaltingNumber(lane_id)
total_on_lane = traci.lane.getLastStepVehicleNumber(lane_id)
lane_vehicle_ids = traci.lane.getLastStepVehicleIDs(lane_id)

print(f"\n--- Lane: {lane_id} (vehicle {veh_id}'s current lane) ---")
print(f"Halted (queued) count: {queue}")
print(f"Total vehicle count:   {total_on_lane}")
print("Vehicles on this lane, with individual speeds:")
for lv_id in lane_vehicle_ids:
    lv_speed = traci.vehicle.getSpeed(lv_id)
    halted_flag = "HALTED" if lv_speed < 0.1 else "moving"
    print(f"  {lv_id}: {lv_speed:.2f} m/s ({halted_flag})")

tls_id = tls_ids[0]
phase_index = traci.trafficlight.getPhase(tls_id)
state = traci.trafficlight.getRedYellowGreenState(tls_id)

print(f"\n--- Traffic light: {tls_id} ---")
print(f"Phase index: {phase_index}")
print(f"Light state: {state}")
print("(one character per controlled link, in link-index order:")
print(" r/R = red, y/Y = yellow, g = green minor/yield, G = green major)")

traci.close()
