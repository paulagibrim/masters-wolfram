from automaton import CellularAutomaton
from utils import paint

class ComposedAC(CellularAutomaton):
    def __init__(self, size:int, steps:int, rule:int, rule2:int, begin_type:str):
        # Set the second rule
        self._rule2 = None
        self.__set_rule(rule2)

        # Call the parent constructor
        super().__init__(size, steps, rule, begin_type)




    def __set_rule(self, rule):
        """
        Set the rule of the cellular automaton.
        """
        super()._validate_rule(rule)
        # if rule is None:
        #     raise ValueError(
        #         paint('red', '[ERROR] Invalid rule specified.\n'),
        #         "Please use a valid rule number."
        #     )
        self._rule2 = super()._get_rule_obj(rule)

    def _evolve(self, step):
        """
        Calculate the next state of the automaton for a given step.
        :param step: int, the current step in the simulation.
        """
        super()._evolve(step)

        next_state = self._grid[step + 1].copy()
        temp_state = next_state.copy()

        for cell in range(self._size):
            left = next_state[(cell - 1) % self._size]
            center = next_state[cell]
            right = next_state[(cell + 1) % self._size]

            neighbors = (left, center, right)
            temp_state[cell] = self._rule2.get_rule_dict()[neighbors]

        # Copia o resultado final para a matriz do grid
        self._grid[step + 1] = temp_state.copy()

    def reset(self, begin_type: str = 'fixed', rule: int = None, rule2:int = None, index: int = None):
        super().reset(begin_type, rule, index)
        self.__set_rule(rule2)

    def _get_path_name(self):
        path = ''
        class_id_rule1 = self._get_class(self._rule.get_number()).get_id()
        class_id_rule2 = self._get_class(self._rule2.get_number()).get_id()

        class_label_rule1 = self._get_class(self._rule.get_number()).get_label()
        class_label_rule2 = self._get_class(self._rule2.get_number()).get_label()

        if class_id_rule1 > class_id_rule2:
            path += class_label_rule2
            path += ' + ' + class_label_rule1 + '/'

        else:
            path += class_label_rule1
            path += ' + ' + class_label_rule2 + '/'

        label_rule1 = self._rule.get_label()
        label_rule2 = self._rule2.get_label()

        path += label_rule1 + ' + ' + label_rule2 + '.png'
        return path










