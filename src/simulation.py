import os
from automaton import CellularAutomaton
from simulation_type import SimulationType
from src.composed_ac import ComposedAC
from utils import paint
from classes import HOMOGENEOUS, PERIODIC, CHAOTIC, COMPLEX

class Simulation:
    def __init__(self, sim_type:SimulationType, scale: int = 4, size:int = 100, steps: int = 200):
        self.__sim_type = self.__validate_sim_type(sim_type)
        self.__ca = None
        self.__scale = scale
        self.__size = size
        self.__steps = steps

        #self.__rule = rule # Rule to be simulated, if sim_type is 'single'

    @staticmethod
    def __validate_sim_type(sim_type):
        """Validate the simulation type"""
        if not isinstance(sim_type, SimulationType):
            raise ValueError(
                "\033[31m[ERROR] Invalid 'sim_type' specified.\033[0m\n Please use a SimulationType object."
            )

        else:
            return sim_type


    @staticmethod
    def __validate_image_output(show: bool, save: bool, debug: bool):
        """Validate the show and save parameters"""
        if not isinstance(show, bool) or not isinstance(save, bool) or not isinstance(debug, bool):
            raise ValueError(
                paint('red', '[ERROR] Invalid parameters specified.\n'),
                "Please use a boolean value for these parameters."
            )

    def __handle_image_output(self, show: bool, save: bool, debug: bool):
        """Return the show and save parameters"""
        self.__validate_image_output(show, save, debug)

        if show:
            self.__ca.show_image(scale=self.__scale)
            if debug:
                print(paint('yellow', '[INFO] Image opened:' + os.path.basename(self.__ca.get_label())))
        if save:
            self.__ca.save_image(scale=self.__scale)
            if debug:
                print(paint('yellow', '[INFO] Image saved:' + self.__ca.get_label()))


    def run(self, show: bool = False, save: bool = True, debug: bool = False, begin_type: str = 'random'):
        """Run the simulation"""
        self.__validate_image_output(show, save, debug)

        self.__ca = CellularAutomaton(self.__size, self.__steps, rule=0, begin_type='fixed')
        # self.__ca.calculate_previous_execs()

        # Write some debug information on the console
        self.__sim_type.info(debug=debug)

        # Get the number of executions
        execs = self.__sim_type.get_execs()

        for exec in range(execs):
            if debug:
                print(paint('yellow', '========== DEBUG INFO =========='))
                print(paint('yellow', '[INFO] Executing simulation ' + str(exec + 1) + ' of ' + str(execs)))
                print(paint('yellow', '==============================='))

            if self.__sim_type.name == 'single':
                # @FIXME: O path que a imagem é salva não está bom - a organização de pastas fica feia - podre
                # Get the rule to be simulated
                rule = self.__sim_type.get_rule()

                # Run the simulation
                self.__ca.reset(rule=rule, rule2=None, begin_type=begin_type, index=exec)
                self.__ca.run()
                self.__handle_image_output(show, save, debug)
                prev = self.__ca.get_previous_execs()
                self.__ca.set_previous_execs(prev-1)

            elif self.__sim_type.name == 'all':
                for i in range(256):
                    self.__ca.reset(rule=i, begin_type='fixed', index=exec)
                    self.__ca.run()
                    self.__handle_image_output(show, save, debug)

            elif self.__sim_type.name == 'complete':
                self.__ca = ComposedAC(self.__size, self.__steps, rule=0, rule2=0, begin_type='fixed')
                for i in range(256):
                    for j in range(256):
                        if i == j:
                            continue
                        else:
                            self.__ca.reset(rule=i, rule2=j, index=exec, begin_type='fixed')
                            self.__ca.run()
                            self.__handle_image_output(show, save, debug)

            elif self.__sim_type.name[:7] == 'custom-' and self.__sim_type.name[8] == '-':
                c1, c2 = self.__sim_type.get_chosen_classes()
                self.__ca = ComposedAC(self.__size, self.__steps, rule=0, rule2=0, begin_type='fixed')
                for rule1 in c1.get_rules():
                    for rule2 in c2.get_rules():
                        if rule1 == rule2:
                            continue
                        else:
                            self.__ca.reset(rule=rule1, rule2=rule2, begin_type='fixed', index=exec)
                            self.__ca.run()
                            self.__handle_image_output(show, save, debug)


    # DEBUG METHODS
    # def debug_simulations