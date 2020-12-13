"""
The module contains observation related classes
"""

import os
import shutil
import ntpath
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler
from common.utils import Utils


class Watcher(object):
    """
    Observe specific folder for an event
    """
    def __init__(self, obj):
        self.log = obj.log
        self._src_path = obj.path
        self.__event_handler = Handler(obj)
        self.__observer = Observer()

    def run(self):
        """
        Main function to start the observation
        :return: None
        """
        self.start()
        try:
            while self.__observer.is_alive():
                self.__observer.join(1)
        except KeyboardInterrupt:
            self.stop()
            self.log.debug(f'Application stopped. Got key board interrupt!')

    def start(self):
        """
        Starts the observation
        :return: None
        """
        self._schedule()
        self.__observer.start()
        self.log.info(f'Folder "{self._src_path}" is under observation.')

    def stop(self):
        """
        Stops the observation on keyboard interrupt
        :return: None
        """
        self.__observer.stop()
        self.__observer.join()

    def _schedule(self):
        """
        Schedule the handler to provided path
        :return: None
        """
        self.__observer.schedule(self.__event_handler, self._src_path, recursive=True)


class Handler(RegexMatchingEventHandler):
    """
    Handle specific event and perform operations accordingly
    """
    def __init__(self, obj):
        self.obj = obj
        self.log = obj.log
        self.utils_obj = Utils(self.obj)
        super().__init__(obj.reg_ex)

    def on_created(self, event):
        """
        Gets triggered on file create/copy/drag event
        :param event: obj
        :return: None
        """
        if any([True if '.txt' in reg_ex else False for reg_ex in self.obj.reg_ex]):
            self.text_file_process(event)
        elif any([True if '.zip' in reg_ex else False for reg_ex in self.obj.reg_ex]):
            self.zip_file_process(event)
        else:
            self.log.error('files type of provided regular expressions are not handled')

    def text_file_process(self, event):
        """
        Handles '.txt' files
        :param event: Obj
        :return: None
        """
        self.log.info(f'New text file found under observation: "{event.src_path}"')
        project_dir = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
        monitor_head, monitor_tail = ntpath.split(event.src_path)
        try:
            shutil.move(event.src_path, project_dir)
        except shutil.Error as er:
            if 'already exists' in str(er):
                os.rename(os.path.join(project_dir, monitor_tail),
                          os.path.join(project_dir, 'XXwatcher_tempXX.txt'))
                shutil.move(event.src_path, project_dir)
                os.remove(os.path.join(project_dir, 'XXwatcher_tempXX.txt'))
        head, tail = ntpath.split(event.src_path)
        zip_file, password = self.utils_obj.create_zip(tail)
        self.utils_obj.move_file(os.path.join(project_dir, zip_file), self.obj.dest_folder_path)
        self.log.info(f'Observation continue. .')

    def zip_file_process(self, event):
        """
        Handles '.zip' files
        :param event: Obj
        :return: None
        """
        head, tail = ntpath.split(event.src_path)
        self.log.info(f'New text file found under observation: "{event.src_path}"')
        password = self.utils_obj.decode_password(tail)
        filename, file_data = self.utils_obj.read_zip(event.src_path, password)
        pii_filtered_data = self.utils_obj.perform_pii(file_data)
        self.utils_obj.create_pii_filtered_file(self.obj.dest_folder_path, filename, pii_filtered_data)
        self.log.info(f'Observation continue. .')