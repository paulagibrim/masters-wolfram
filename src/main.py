import automaton as at
# from ace_classes import HOMOGENIOUS, PERIODIC, CHAOTIC, COMPLEX

ca = at.CellularAutomaton(100, 100, rule=110)

ca.run()
ca.show_image(scale=10)
# ca.save_image(scale=4)

# ca.test(scale=10).show()