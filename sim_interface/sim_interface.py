import os

import traci

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SUMOCFG_PATH = os.path.join(SCRIPT_DIR, "..", "sim.sumocfg")

traci.start(["sumo", "-c", SUMOCFG_PATH])

for step in range(200):
    traci.simulationStep()

    queue_lengths = {
        lane_id: traci.lane.getLastStepHaltingNumber(lane_id)
        for lane_id in traci.lane.getIDList()
    }

    tls_phases = {
        tls_id: traci.trafficlight.getPhase(tls_id)
        for tls_id in traci.trafficlight.getIDList()
    }

    vehicle_states = {
        veh_id: {
            "position": traci.vehicle.getPosition(veh_id),
            "speed": traci.vehicle.getSpeed(veh_id),
        }
        for veh_id in traci.vehicle.getIDList()
    }

    print(
        f"step={step} "
        f"lanes={len(queue_lengths)} "
        f"tls={len(tls_phases)} "
        f"vehicles={len(vehicle_states)}"
    )

traci.close()
