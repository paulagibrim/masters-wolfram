import simulation as sim
import simulation_type as stype

TIMES_TO_RUN = 1


sim_type = stype.SimulationType('complete', execs=TIMES_TO_RUN)
simulate = sim.Simulation(sim_type, scale=10, size=100, steps=200)
simulate.run(debug=True)
    
