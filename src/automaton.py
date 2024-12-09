from rules import rules
from classes import HOMOGENEOUS, PERIODIC, CHAOTIC, COMPLEX
from PIL import Image

import numpy as np

import os

class CellularAutomaton:
    def __init__(self, size: int, steps: int, rule: int, rule2: int=None, begin_type: str='random', zip_mode: bool=False):
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
        self.__zip_mode = None
        self.__rule = None
        self.__rule2 = None
        self.__begin_type = None

        self.__set_rules(rule, rule2)
        self.__label = ''

        ## LABEL INITIALIZATION ##
        self.__set_label()

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
            raise ValueError(f"Rule dictionary is missing combinations: {missing_combinations}")

    def __validate_zip_mode(self, zip_mode):
        """
        Validate the zip mode.
        """
        if zip_mode and self.__rule2 is None:
            raise ValueError("Zip mode requires both rule and rule2.")
        if zip_mode and self.__begin_type == 'center':
            raise ValueError("Zip mode is not compatible with center begin type.")
        self.__zip_mode = zip_mode

    def __validate_begin_type(self, begin_type):
        """
        Validate the begin type.
        """
        if begin_type not in ['random', 'center']:
            raise ValueError("Invalid begin_type. Use 'random' or 'center'.")
        else:
            self.__begin_type = begin_type

    def __validate_creation(self, begin_type):
        """
        Validate the creation of the cellular automaton.
        """
        self.__validate_begin_type(begin_type)
        self.__validate_zip_mode(self.__zip_mode)

    def __validate_rule(self, rule):
        """
        Validate the rule of the cellular automaton.
        """
        if rule not in rules:
            raise ValueError("Invalid rule number. Must be in the range 0-255.")
        
    def __validate_path(self, path):
        """
        Validate the path of the image.
        """
        if not isinstance(path, str):
            raise ValueError("Invalid path. Must be a string.")
        
        # if not path.endswith('.png'):
        #     raise ValueError("Invalid path. Must be a PNG file.")
        
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            print(f"Creating directory: {directory}")
            os.makedirs(directory)  # Cria o diretório se ele não existir

    #### RULE GENERATION METHODS ####

    @staticmethod
    def __generate_rule_dict(rule_number):
        """
        Generate the dictionary for a given rule number in Wolfram's 1D automata.
        :param rule_number: int, the rule ID (0-255).
        :return: dict, mapping of neighbor states to next state.
        """
        binary_representation = f"{rule_number:08b}"
        combinations = [
            (0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1),
            (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1),
        ]
        return {
            combo: int(binary_representation[7 - i])
            for i, combo in enumerate(combinations)
        }
    
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

    def __evolve(self, step):
        for cell in range(self.__size):
            left = self.__grid[step, (cell - 1) % self.__size]
            center = self.__grid[step, cell]
            right = self.__grid[step, (cell + 1) % self.__size]

            neighbors = (left, center, right)

            self.__grid[step + 1, cell] = self.__rule.get_rule_dict()[neighbors]

    def get_grid(self):
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

    def __initialize_grid(self):
        """
        Initialize the grid with a random state.
        """
        grid = np.zeros((self.__steps, self.__size), dtype=bool)
        if self.__begin_type == 'random':
            grid = self.__set_initial_state(np.random.randint(0, 2, self.__size, dtype=bool), grid)

        elif self.__begin_type == 'center':
            init = np.zeros(self.__size, dtype=bool)
            init[self.__size//2] = 1
            grid = self.__set_initial_state(init, grid)

        return grid

    def __set_initial_state(self, initial_state, grid):
        """
        Set the initial state of the grid.
        """
        if len(initial_state) != self.__size:
            raise ValueError("Initial state must have the same size as the grid.")
        grid[0] = initial_state
        return grid

    # Possivelmente privado
    def reset(self, begin_type='random'):
        self.__validate_creation(begin_type)
        
        if begin_type == 'random':
            self.__grid[0] = np.random.randint(0, 2, self.__size, dtype=bool)
        elif begin_type == 'center':
            self.__grid[0] = 0
            self.__grid[0, self.__size // 2] = 1
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

        self.__get_image(scale).save(self.__label, 'PNG')

    def show_image(self, scale=1):
        """
        Show the grid as an image.
        """
        self.__get_image(scale).show()

    @staticmethod
    def __get_class(rule):
        """
        Return the class of the cellular automaton.
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
            raise ValueError("[!] Rule: {} does not match any class. Something went wrong.".format(rule))
    
    def __set_label(self):
        """
        Set the label of the cellular automaton.
        """
        self.__label = '../results/'
        self.__validate_path(self.__label)

        if self.__rule2 is not None:
            if  self.__get_class(self.__rule.get_number()).get_id() > self.__get_class(self.__rule2.get_number()).get_id():
                self.__label += self.__get_class(self.__rule2.get_number()).get_label()
                self.__label += ' + ' + self.__get_class(self.__rule.get_number()) + '/'
                
            else:
                self.__label += self.__get_class(self.__rule.get_number()).get_label()
                self.__label += ' + ' + self.__get_class(self.__rule2.get_number()) + '/'
            
            self.__validate_path(self.__label)
            self.__label += self.__rule.get_label() + ' + ' + self.__rule2.get_label() + '.png'
    	
        else:
            self.__label += self.__get_class(self.__rule.get_number()).get_label() + '/'
            self.__validate_path(self.__label)
            self.__label += self.__rule.get_label() + '.png'

    ### BINARY LIFTING METHODS ###

    def find_step(self, looking_for: int, initial_state):
        """
        Find the step of the cellular automaton.
        """
        self.__steps = looking_for + 1
        grid = np.zeros((self.__steps, self.__size), dtype=bool)
        grid = self.__set_initial_state(initial_state, grid)
        self.run()

        return self.__grid[looking_for]