import os
import numpy as np
from automaton import CellularAutomaton  # Assumindo que a classe original esteja em um arquivo separado

class PerturbedCellularAutomaton(CellularAutomaton):
    def __init__(self, original_automaton: CellularAutomaton):
        """
        Construtor que cria uma cópia perturbada de um autômato celular existente.

        :param original_automaton: Instância de CellularAutomaton para ser copiada e perturbada.
        """
        # Copia os atributos da instância original
        super().__init__(
            size=original_automaton._CellularAutomaton__size,
            steps=original_automaton._CellularAutomaton__steps - 1,
            rule=original_automaton._CellularAutomaton__rule.get_number(),
            rule2=(
                original_automaton._CellularAutomaton__rule2.get_number()
                if original_automaton._CellularAutomaton__rule2 is not None
                else None
            ),
            begin_type='fixed'  # Tipo de início fixo para manter a cópia fiel
        )

        # Copia o grid do autômato original
        self.__grid = np.copy(original_automaton._CellularAutomaton__grid)

        # Perturba a célula central da linha 0
        center = self._CellularAutomaton__size // 2
        self.__grid[0, center] = not self.__grid[0, center]

        # Executa a simulação a partir do grid perturbado
        self.run()


