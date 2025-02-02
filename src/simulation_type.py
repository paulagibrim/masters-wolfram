from classes import Class
from utils import paint

class SimulationType:
    def __init__(self, name:str, rule=None, execs:int = 1): #, class1:Class=None):
        self.__name = self.__validate_type(name)
        self.__execs = execs
        
        if self.__name == 'single':
            self.__rule = rule

        # if self.__name == 'complete':
        #     self.__execs = execs

        # @TODO: Implement the custom parameter asking for classes
        # if self.__name[:7] == 'custom-':
        #     self.__execs = execs

    @staticmethod
    def __validate_type(name: str):
        """Validate the simulation type"""
        name = name.lower()

        # @FIXME: ARRUMAR O TIPO CUSTOM-M-N
        # print(name)
        if name not in ['single', 'all', 'complete'] and name[:7] != 'custom-':
            raise ValueError(
                paint('red','[ERROR] Invalid \'type\' specified.\n'),
                "Please use one of the following options:\n"
                "- 'single': Run the simulation for a specified rule. \n"
                "- 'all': Run the simulation for all Wolfram Rules.\n"
                "- 'complete': Run all possible compositions between all Wolfram Rules.\n"
                # "- 'custom-1-1': Run a custom simulation with a pair of rules from Wolfram's homogeneous class.\n"
                # "- 'custom-2-2': Run a custom simulation with a pair of rules from Wolfram's periodic class.\n"
                # "- 'custom-3-3': Run a custom simulation with a pair of rules from Wolfram's chaotic class.\n"
                # "- 'custom-4-4': Run a custom simulation with a pair of rules from Wolfram's complex class.\n"
                "- 'custom-n-m': Run a custom composition simulation between all rules from class n and class m."
            )
        else:
            return name

    def __str__(self):
        return f"Simulation type: {self.__name}\n Executions: {self.__execs}" if self.__name != 'single' else f"Simulation type: {self.__name}\n Rule: {self.__rule}\n Executions: {self.__execs}"


    def info(self, debug: bool = False):
        if debug:
            print(paint('yellow','========== DEBUG INFO =========='))
            print(paint('yellow', str(self)))
            print(paint('yellow','================================'))

    def get_rule(self):
        return self.__rule

    @property
    def name(self):
        return self.__name

    @staticmethod
    def __validate_classes(c1, c2):
        if c1 not in [1, 2, 3, 4] or c2 not in [1, 2, 3, 4]:
            raise ValueError(
                paint('red',"[ERROR] Invalid 'classes' specified.\n"),
                paint('white', "Please choose between 1 and 4 for each class.")
            )
        else:
            return Class(c1), Class(c2)

    def get_chosen_classes(self):
        if self.__name[:7] == 'custom-' and self.__name[8] == '-':
            c1, c2 = self.__validate_classes(int(self.__name[7]), int(self.__name[9]))
            return c1, c2

    def get_execs(self):
        return self.__execs