from automaton import CellularAutomaton

class Simulation:
    def __init__(self, ca: CellularAutomaton, scale: int = 4):
        self.ca = ca
        self.scale = scale


    def run(self, show: bool = True, save: bool = True):
        self.ca.run()
        if show:
            self.ca.show_image(scale=self.scale)
        if save:
            self.ca.save_image(scale=self.scale)