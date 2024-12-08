import simulation as sim
import automaton as at
import binary_lifting as bl

# ca = at.CellularAutomaton(100, 200, rule=110)
#
# simulate = sim.Simulation(ca, scale=10)
#
# simulate.run(save=True)
ca = at.CellularAutomaton(20, 10, rule=110)
init_state = tuple(ca.get_grid()[0])
# print (tuple(int(x) for x in init_state))
# simulate = sim.Simulation(ca, scale=10)
# # simulate.run(save=False)
result = tuple(int(x) for x in ca.find_step(987654321234, init_state).astype(int))
print(result)
# # result = tuple(int(x) for x in ca.find_step(2).astype(int))
# # print(result)
# # result = tuple(int(x) for x in ca.find_step(3).astype(int))
# # print(result)
# # result = tuple(int(x) for x in ca.find_step(4).astype(int))
# # print(result)



# # print()
# #
# binary = bl.BinaryLifting(110, size=20, max_steps=2**40)
# # print(tuple(int(x) for x in binary.find_step(0, initial_state=init_state)))
# print(binary.find_step(987654321234, initial_state=init_state))
#
