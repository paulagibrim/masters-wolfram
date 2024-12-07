import simulation as sim
import automaton as at

ca = at.CellularAutomaton(100, 200, rule=110)

simulate = sim.Simulation(ca, scale=10)

simulate.run(save=True)