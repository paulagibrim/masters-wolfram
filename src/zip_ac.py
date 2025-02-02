from automaton import CellularAutomaton

class ZipAC(CellularAutomaton):
    def __init__(self, size: int, steps: int, rule: int, rule2: int, begin_type: str='random', index:int=None):
        super().__init__(size, steps, rule=rule, rule2=rule2, begin_type=begin_type, index=index)

