from rules import rules
from classes import HOMOGENEOUS, PERIODIC, CHAOTIC, COMPLEX
from PIL import Image

import numpy as np

import os

class CellularAutomaton:
    def __init__(self, size: int, steps: int, rule: int, rule2: int=None, begin_type: str='random', zip_mode: bool=False, index:int=None):
        """
        Constructor for the CellularAutomaton class.

        :param size: int, number of cells (grid width).
        :param steps: int, number of steps (time stamps) to simulate.
        :param rule: int, maps the current state of the cell and its neighbors to the next state.
        :param rule2: int (optional), a second rule for alternation (zip mode).
        :param begin_type: str, initial state of the cells, 'random' or 'center'.
        :param zip_mode: bool, whether to alternate between two rules at each step.
        """

        self.__size = size
        self.__steps = steps + 1
        self.__zip_mode = None # @FIXME: Fazer zip_mode com herança
        self.__rule = None
        self.__rule2 = None
        self.__begin_type = None
        self.__label = ''
        self.__index = index
        self.__previous_execs = None
        self.__validate_path('../results/')
        self.calculate_previous_execs()

        ## RULE INITIALIZATION ##
        self.__set_rules(rule, rule2)

        ## LABEL INITIALIZATION ##
        self.__set_label()

        # @FIXME: Validate the begin type, use as return value
        ## VALIDATION ##
        self.__validate_creation(begin_type)
        
        ## GRID INITIALIZATION ##
        self.__grid = self.__initialize_grid()



    #### VALIDATION METHODS ####

    @staticmethod 
    def __validate_scale(scale):
        """
        Validate the scale for image generation.
        """
        if not isinstance(scale, int) or scale < 1:
            raise ValueError("Scale must be an integer greater than 0.")

    @staticmethod
    def __validate_rule_dict(rule_dict):
        """
        Validate that the rule dictionary defines all 8 possible neighbor combinations.
        :param rule_dict: dict, mapping of neighbor states to next state.
        """
        combinations = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
        missing_combinations = [combo for combo in combinations if combo not in rule_dict]
        if missing_combinations:
            raise ValueError(f"\033[31m[ERROR] Rule dictionary is missing combinations: {missing_combinations}\033[0m")

    def __validate_zip_mode(self, zip_mode):
        """
        Validate the zip mode.
        """
        if zip_mode and self.__rule2 is None:
            raise ValueError("\033[31m[ERROR] Zip mode requires both rule and rule2.\033[0m")
        if zip_mode and self.__begin_type == 'center':
            raise ValueError("\033[31m[ERROR] Zip mode is not compatible with center begin type.\033[0m")
        self.__zip_mode = zip_mode

    def __validate_begin_type(self, begin_type):
        """
        Validate the beginning type.
        """
        if begin_type not in ['random', 'center', 'fixed']:
            raise ValueError("\033[31m[ERROR] Invalid begin_type. Use 'random', 'center' or 'fixed'.\033[0m")
        else:
            self.__begin_type = begin_type

    def __validate_creation(self, begin_type):
        """
        Validate the creation of the cellular automaton.
        """
        self.__validate_begin_type(begin_type)
        self.__validate_zip_mode(self.__zip_mode)

    @staticmethod
    def __validate_rules(rule):
        """
        Validate the rule of the cellular automaton.
        """
        if rule not in rules:
            raise ValueError("\033[31m[ERROR] Invalid rule number. Must be in the range 0-255.\033[0m")

    @staticmethod
    def __validate_path(path):
        """
        Validate the path of the image.
        """
        if not isinstance(path, str):
            raise ValueError("\033[31m[ERROR] Invalid path. Must be a string.\033[0m")
        
        # if not path.endswith('.png'):
        #     raise ValueError("Invalid path. Must be a PNG file.")
        
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            print(f"Creating directory: {directory}")
            os.makedirs(directory)  # Cria o diretório se ele não existir

    @staticmethod
    def __validate_class(rule):
        """
        Validate the class of the cellular automaton.
        """
        if rule in HOMOGENEOUS.get_rules():
            return HOMOGENEOUS
        elif rule in PERIODIC.get_rules():
            return PERIODIC
        elif rule in CHAOTIC.get_rules():
            return CHAOTIC
        elif rule in COMPLEX.get_rules():
            return COMPLEX
        else:
            # raise Warning("[!] Rule: {} does not match any class.".format(rule))
            raise ValueError('\033[31m[ERROR] Rule:', rule ,'does not match any class. Something went wrong.' + '\033[0m')

    #### RULE GENERATION METHODS ####

    @staticmethod
    def __generate_rule_dict(rule_number):
        return rules[rule_number].get_rule_dict()
    
    def __get_rule_obj(self, rule):
        """
        Set the rule of the cellular automaton.
        """
        rule = rules[rule]
        self.__validate_rule_dict(rule.get_rule_dict())

        return rule
    
    def __set_rules(self, rule, rule2=None):
        """
        Set the rule of the cellular automaton.
        """
        self.__rule = self.__get_rule_obj(rule)
        self.__rule2 = self.__get_rule_obj(rule2) if rule2 is not None else None


    #### SIMULATION METHODS ####

    def __evolve(self, step):
        """
        Calculate the next state of the automaton for a given step.
        :param step: int, the current step in the simulation.
        """
        next_state = self.__grid[step].copy()  # Cria uma cópia temporária para evitar alterações diretas

        for cell in range(self.__size):
            # Set the neighbors of the cell, using boundary conditions
            left = self.__grid[step, (cell - 1) % self.__size]
            center = self.__grid[step, cell]
            right = self.__grid[step, (cell + 1) % self.__size]

            # Apply the first rule
            neighbors = (left, center, right)
            next_state[cell] = self.__rule.get_rule_dict()[neighbors]

        # Copia o estado atualizado para o grid
        self.__grid[step + 1] = next_state.copy()

        # Se houver uma segunda regra, aplicamos em um segundo passo, mas SEM alterar diretamente 'next_state'
        if self.__rule2 is not None:
            temp_state = next_state.copy()

            for cell in range(self.__size):
                left = next_state[(cell - 1) % self.__size]
                center = next_state[cell]
                right = next_state[(cell + 1) % self.__size]

                neighbors = (left, center, right)
                temp_state[cell] = self.__rule2.get_rule_dict()[neighbors]

            # Copia o resultado final para a matriz do grid
            self.__grid[step + 1] = temp_state.copy()

    def __get_grid(self):
        """
        Return the grid.
        """
        return self.__grid

    def run(self):
        """
        Run the simulation.
        """
        for step in range(self.__steps - 1):
            self.__evolve(step)

    def get_initial_state(self):
        """
        Return the initial state of the grid.
        """
        return self.__grid[0]

    def set_initial_state(self, initial_state):
        """
        Set the initial state of the grid.
        """
        self.__set_initial_state(initial_state, self.__grid)
    

    ### INITIALIZATION METHODS ###

    def __initialize_grid(self):
        """
        Initialize the grid with a state.
        """
        grid = np.zeros((self.__steps, self.__size), dtype=bool)
        if self.__begin_type == 'random' or self.__begin_type == 'fixed':
            grid = self.__set_initial_state(np.random.randint(0, 2, self.__size, dtype=bool), grid)

        elif self.__begin_type == 'center':
            init = np.zeros(self.__size, dtype=bool)
            init[self.__size//2] = 1
            # init[self.__size // 2] = !init[self.__size // 2]
            grid[0] = self.__set_initial_state(init, grid)

        return grid

    def __set_initial_state(self, initial_state, grid):
        """
        Set the initial state of the grid.
        """
        if len(initial_state) != self.__size:
            raise ValueError("Initial state must have the same size as the grid.") # @FIXME: Colocar COR
        grid[0] = initial_state
        # print (grid[0])
        return grid


    def reset(self, begin_type:str ='fixed', rule: int=None, rule2: int=None, zip_mode: bool=False, index:int=None):
        if rule is None:
            raise ValueError("[ERROR] Rule must be specified.") # @FIXME: Colocar COR
        self.__index = index
        self.__set_rules(rule, rule2)
        self.__set_label()
        # self.__zip_mode = zip_mode

        self.__validate_creation(begin_type)
        
        self.__reset_grid()

    def __reset_grid(self):
        if self.__begin_type == 'random':
            self.__grid[0] = np.random.randint(0, 2, self.__size, dtype=bool)
        elif self.__begin_type == 'center':
            self.__grid[0] = 0
            self.__grid[0, self.__size // 2] = 1
        # elif begin_type == 'fixed':
        #     pass
        # else:
        #     raise ValueError("Invalid begin type. Use 'random', 'center' or 'fixed'.")
        self.__grid[1:] = 0

    ### IMAGE GENERATION METHODS ###

    def __get_image_array(self):
        """
        Return the grid as an image.
        """
        return (~self.__grid).astype(np.uint8) * 255
    
    def __get_image(self, scale=1):
        """
        Return the grid as an image.
        """
        self.__validate_scale(scale)
        img_arr = self.__get_image_array()
        return Image.fromarray(np.kron(img_arr, np.ones((scale, scale), dtype=np.uint8)), mode='L')
    
    def save_image(self, scale=1):
        """
        Save the grid as an image.
        """
        self.__validate_path(self.__label)
        self.__get_image(scale).save(self.__label, 'PNG')

    def show_image(self, scale=1):
        """
        Show the grid as an image.
        """
        self.__get_image(scale).show()

    def __get_class(self, rule):
        """
        Return the class of the cellular automaton.
        """
        return self.__validate_class(rule)
    
    def get_label(self):
        """
        Return the label of the cellular automaton.
        """
        return self.__label

    def __set_label(self):
        """
        Set the label of the cellular automaton.
        """

        self.__label = '../results/'

        # Number of previous executions
        # if self.__index == 0:
        #     last_execs = sum(
        #         1 for item in os.listdir('../results')
        #         if os.path.isdir(os.path.join('../results', item)) and 'exec' in item
        #     )

        if self.__index is not None and self.__index >= 0 and self.__previous_execs is not None:
            self.__label += 'exec_' + str((self.__index + self.__previous_execs)) + '/'

        # @TODO: Colocar essas criações de nomes em um método separado
        if self.__rule2 is not None:
            if  self.__get_class(self.__rule.get_number()).get_id() > self.__get_class(self.__rule2.get_number()).get_id():
                self.__label += self.__get_class(self.__rule2.get_number()).get_label()
                self.__label += ' + ' + self.__get_class(self.__rule.get_number()).get_label() + '/'

            else:
                self.__label += self.__get_class(self.__rule.get_number()).get_label()
                self.__label += ' + ' + self.__get_class(self.__rule2.get_number()).get_label() + '/'

            self.__label += self.__rule.get_label() + ' + ' + self.__rule2.get_label() + '.png'

        else:
            self.__label += 'single/'
            self.__label += self.__get_class(self.__rule.get_number()).get_label() + '/'
            self.__label += (self.__rule.get_label() + '_' + str(self.__index) + '.png')


    def calculate_previous_execs(self):
        """
        Calculate the number of previous executions.
        """

        self.__previous_execs = sum(
            1 for item in os.listdir('../results')
            if os.path.isdir(os.path.join('../results', item)) and 'exec' in item
        )

    def set_previous_execs(self, previous_execs):
        """
        Set the number of previous executions
        """

        self.__previous_execs = previous_execs

    def get_previous_execs(self):
        """
        Return the number of previous executions
        """

        return self.__previous_execs