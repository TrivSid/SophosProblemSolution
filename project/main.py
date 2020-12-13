"""
The module contains Main class which starts all operations
"""
import os
import yaml
from lib.observer import Watcher
from common.utils import Utils
from common.utils import Log
from common.utils import ArgumentParser


class ObjGrp(object):
    """
    Used to store other objects
    """
    pass


class Main(object):
    """
    Main class to start the operation
    """

    def __init__(self):
        data = self.read_input()
        self.observe_path = data['observe_path']
        self.dest_folder_path = data['dest_folder_path']
        self.part1 = False
        self.part2 = False
        self.main()

    @staticmethod
    def read_input():
        """
        Reads '.yaml. files
        :return: dict
        """
        with open(os.path.join(os.path.dirname(__file__), 'config', 'input.yaml')) as file:
            input = yaml.load(file, Loader=yaml.FullLoader)
        return input['Data']

    def main(self):
        """
        main folder
        """
        # collect all data to one object
        obj = ObjGrp()
        obj.dest_folder_path = self.dest_folder_path
        obj.observe_path = self.observe_path
        obj.log = Log()
        self.part1, self.part2 = ArgumentParser(obj).get_args()

        # starts the observation based on command line arguments
        obj.log.info(f'---------------------------------OBSERVATION ON-------------------------------------')
        Utils(obj).create_folder(self.dest_folder_path)
        if self.part1:
            obj.path = self.observe_path
            obj.reg_ex = [r'^.*\.txt$']
            Watcher(obj).run()
        elif self.part2:
            obj.path = self.dest_folder_path
            obj.reg_ex = [r'^.*\.zip$']
            Watcher(obj).run()
        else:
            obj.log.info('Tracking disabled for Part1 and Part2.')
