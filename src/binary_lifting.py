import numpy as np

from rules import rules

import math

class BinaryLifting:
    def __init__(self, rule: int, size: int = 20, max_steps: int = 2**64):
        self.__size = size
        self.rule = rules[rule]
        self.max_steps = max_steps
        self.all_possible_values = self.__set_possible_values()
        # print(len(self.all_possible_values))
        # print(2**size)
        # self.mapping_possible_values = self.__generate_mapping_possible_values()
        # print(self.mapping)
        self.pre_processing = self.__generate_pre_processing()
        # print(self.pre_processing)



    def __set_possible_values(self):
        # Gerar todas as combinações possíveis de uma linha de tamanho 'size'
        return [tuple(map(int, f"{i:0{self.__size}b}")) for i in range(2 ** self.__size)]

    def __generate_mapping_possible_values(self):
        mapping = {}
        for row in self.all_possible_values:
            next = []
            for cell in range(self.__size):
                left = row[(cell - 1) % self.__size]
                center = row[cell]
                right = row[(cell + 1) % self.__size]

                neighbors = (left, center, right)

                next.append(self.rule.get_rule_dict()[neighbors])
                #DEBUG
                # print(self.rule.get_rule_dict()[neighbors])

            mapping[row] = tuple(next)

        return mapping

    def __generate_pre_processing(self):
        next = [self.__generate_mapping_possible_values()]

        for pot in range(1, math.ceil(math.log2(self.max_steps))):
            next.append({})
            for value, pos in enumerate(self.all_possible_values):
                aux = next[pot - 1][pos]
                next[pot][pos] = next[pot - 1][aux]

        return next

    def find_step(self, step: int, initial_state: tuple = None):
        if initial_state is None:
            initial_state = tuple(np.random.randint(0, 2, self.__size))

        actual = initial_state
        looking_for = step

        for pot in range(math.ceil(math.log2(self.max_steps)), -1, -1):
            if 2 ** pot <= looking_for:
                actual = self.pre_processing[pot][actual]
                looking_for -= 2 ** pot

        return actual

