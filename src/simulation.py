import os
from automaton import CellularAutomaton
from simulation_type import SimulationType

class Simulation:
    def __init__(self, sim_type:SimulationType, scale: int = 4, size:int = 100, steps: int = 200):
        self.__sim_type = self.__validate_sim_type(sim_type)
        self.__ca = None
        self.__scale = scale
        self.__size = size
        self.__steps = steps

        #self.__rule = rule # Rule to be simulated, if sim_type is 'single'

    @staticmethod
    def __validate_sim_type(self, sim_type):
        """Validate the simulation type"""
        if not isinstance(sim_type, SimulationType):
            raise ValueError(
                "\033[31m[ERROR] Invalid 'sim_type' specified.\033[0m\n Please use a SimulationType object."
            )

        else:
            return sim_type


    @staticmethod
    def __validate_image_output(self, show: bool, save: bool, debug: bool):
        """Validate the show and save parameters"""
        if not isinstance(show, bool) or not isinstance(save, bool) or not isinstance(debug, bool):
            raise ValueError(
                "\033[31m[ERROR] Invalid 'show', 'save' or 'debug' parameter specified.\033[0m\n\n"
                "Please use a boolean value for these parameters."
            )

    def __handle_image_output(self, show: bool, save: bool, debug: bool):
        """Return the show and save parameters"""
        self.__validate_image_output(show, save, debug)

        if show:
            self.__ca.show_image(scale=self.__scale)
            if debug:
                print('\033[32m[INFO] Image opened:', os.path.basename(self.__ca.get_label()),'\033[0m')
        if save:
            self.__ca.save_image(scale=self.__scale)
            if debug:
                print('\033[32m[INFO] Image saved:', self.__ca.get_label(),'\033[0m')


    def run(self, show: bool = False, save: bool = True, debug: bool = False, begin_type: str = 'random'):
        """Run the simulation"""
        self.__validate_image_output(show, save, debug)

        if self.__sim_type.name == 'single':
            _, rule = self.__sim_type.info(debug=debug)
            self.__ca = CellularAutomaton(self.__size, self.__steps, rule=rule, begin_type=begin_type)
            self.__ca.run()
            self.__handle_image_output(show, save, debug)
        
        elif self.__sim_type.name == 'all':
            for i in range(256):
                _ = self.__sim_type.info(debug=debug)
                self.__ca = CellularAutomaton(self.__size, self.__steps, rule=i, begin_type=begin_type)
                self.__ca.run()
                self.__handle_image_output(show, save, debug)
                self.__ca.reset(begin_type=begin_type)
        
        elif self.__sim_type.name == 'complete':
            _, execs = self.__sim_type.info(debug=debug)
            self.__ca = CellularAutomaton(self.__size, self.__steps, rule=0, rule2=0, begin_type='fixed')
            for exec in range(execs):
                if debug:
                    print('\033[32m========== DEBUG INFO ==========\033[0m')
                    print('\033[32m[INFO] Executing simulation', exec+1, 'of', execs, '\033[0m')
                    print('\033[32m===============================\033[0m')
                for i in range(256):
                    for j in range(256):
                        if i == j:
                            continue
                        else:
                            # self.__ca = CellularAutomaton(self.__size, self.__steps, rule=i, rule2=j, index=exec, begin_type='random')
                            self.__ca.reset(rule=i, rule2=j, index=exec, begin_type='fixed')
                            # print(self.__ca.get_initial_state())
                            self.__ca.run()
                            self.__handle_image_output(show, save, debug)

        
    
