from token import NUMBER

import simulation as sim
import simulation_type as stype

TIMES_TO_RUN = 2
SCALE = 2
NUMBER_OF_CELLS = 100
NUMBER_OF_GENERATIONS = 200

# sim_type = stype.SimulationType('single', execs=TIMES_TO_RUN, rule=30)
# simulate = sim.Simulation(sim_type, scale=SCALE, size=NUMBER_OF_CELLS, steps=NUMBER_OF_GENERATIONS)
# simulate.run(debug=True)

# sim_type = stype.SimulationType('all', execs=TIMES_TO_RUN)
# simulate = sim.Simulation(sim_type, scale=SCALE, size=NUMBER_OF_CELLS, steps=NUMBER_OF_GENERATIONS)
# simulate.run(debug=True)

sim_type = stype.SimulationType('custom-1-1', execs=TIMES_TO_RUN)
simulate = sim.Simulation(sim_type, scale=SCALE, size=NUMBER_OF_CELLS, steps=NUMBER_OF_GENERATIONS)
simulate.run(debug=True)

# sim_type = stype.SimulationType('custom-2-2', execs=TIMES_TO_RUN)
# simulate = sim.Simulation(sim_type, scale=SCALE, size=NUMBER_OF_CELLS, steps=NUMBER_OF_GENERATIONS)
# simulate.run(debug=True)

# sim_type = stype.SimulationType('custom-3-3', execs=TIMES_TO_RUN)
# simulate = sim.Simulation(sim_type, scale=SCALE, size=NUMBER_OF_CELLS, steps=NUMBER_OF_GENERATIONS)
# simulate.run(debug=True)

# sim_type = stype.SimulationType('custom-4-4', execs=TIMES_TO_RUN)
# simulate = sim.Simulation(sim_type, scale=SCALE, size=NUMBER_OF_CELLS, steps=NUMBER_OF_GENERATIONS)
# simulate.run(debug=True)