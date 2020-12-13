"""
The module contains common utility operations
"""

import os
import re
import sys
import shutil
import logging
import pyzipper
import datetime
from datetime import timezone
from optparse import OptionParser


class Log(object):
    """
    Class perform logging operation
    """
    def __init__(self):
        dt = datetime.datetime.now()
        name = dt.strftime("%Y_%m_%d_%I_%M_%S_%p")
        self.logging = logging
        self.logging.basicConfig(level=logging.DEBUG,
                                 format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
                                 datefmt='%m-%d %H:%M',
                                 filename=os.path.join(os.path.split(os.path.dirname(__file__))[0], 'logs',
                                                       'log_observer_' + name + '.txt'),
                                 filemode='w')
        # define a Handler which writes INFO messages or higher to the sys.stderr
        self.console = self.logging.StreamHandler()
        self.console.setLevel(logging.INFO)
        # set a format which is simpler for console use
        self.formatter = self.logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        # tell the handler to use this format
        self.console.setFormatter(self.formatter)
        # add the handler to the root logger
        self.logging.getLogger().addHandler(self.console)
        self.logging.info('---------------------------------OBSERVER APP-------------------------------------')
        self.logging.info(f'Start time: {datetime.datetime.now()}')
        self.logger = logging.getLogger(' log')

    def info(self, text):
        # text is a string
        self.logger.info(text)

    def debug(self, text):
        # text is a string
        self.logger.debug(text)

    def warn(self, text):
        # text is a string
        self.logger.warning(text)

    def error(self, text):
        # text is a string
        self.logger.error(text)

    def critical(self, text):
        # text is a string
        self.logger.critical(text)


class ArgumentParser(object):
    """
    Parse the command line arguments
    """
    def __init__(self, obj):
        self.obj = obj

    def get_args(self):
        """
        Provides command line arguments
        :return: bool
        """
        parser = OptionParser()
        parser.add_option("-t", "--part1",
                          action="store", type="string", dest="part1", default='off',
                          help="pass 'on' to track text file in folder else pass 'off'")
        parser.add_option("-z", "--part2",
                          action="store", type="string", dest="part2", default='off',
                          help="pass 'on' to track zip file in folder else pass 'off'")
        (options, args) = parser.parse_args()

        if options.part1.lower() != 'on' and options.part1.lower() != 'off':
            self.obj.log.error("Invalid commandline argument passed. "
                               "pass 'on' to track text file in folder else pass 'off'")
            exit(0)
        if options.part2.lower() != 'on' and options.part2.lower() != 'off':
            self.obj.log.error("Invalid commandline argument passed. "
                               "pass 'on' to track text file in folder else pass 'off'")
            exit(0)

        options.part1 = True if options.part1.lower() == 'on' else False if options.part1.lower() == 'off' else False
        options.part2 = True if options.part2.lower() == 'on' else False if options.part2.lower() == 'off' else False

        if not options.part1 and not options.part2:
            self.obj.log.error("Both the application mode is disable. "
                               "Pass '--part1 on' or '--part2 on' in commandline argument.")
            exit(0)
        elif options.part1 and options.part2:
            self.obj.log.error("Both the application mode is disable. "
                               "Pass '--part1 on' or '--part2 on' in commandline argument.")
            exit(0)

        return options.part1, options.part2


class Utils(object):
    """
    Contains common utility operations
    """
    def __init__(self, obj):
        self.log = obj.log
        self.dest_folder_path = obj.dest_folder_path

    def create_folder(self, folder_path):
        """
        Creates folder if not present
        :param folder_path: str
        """
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
            self.log.info(f'Folder has been created at "{folder_path}".')
        else:
            self.log.info(f'Folder "{folder_path}" already exists.')
            self.delete_filer_content(folder_path)

    def get_name_password(self):
        """
        Based on UTC epoch timestamp it provides file name and password
        :return: str
        """
        dt = datetime.datetime.now()
        utc_time = dt.replace(tzinfo=timezone.utc)
        password_utc_timestamp = str(utc_time.timestamp()).split('.')[0].encode('ascii')
        filename_dt = dt.strftime("%Y_%m_%d_%I_%M_%S_%p").lower() + '.zip'
        self.log.debug(f'Folder name and password has been decided')
        return filename_dt, password_utc_timestamp

    def delete_filer_content(self, folder):
        """
        Delete the existing folder contents
        :param folder: str
        :return: None
        """
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                self.log.error('Failed to delete %s. Reason: %s' % (file_path, e))
        self.log.info(f'Older files (if present) has been deleted from "{folder}".')

    def create_zip(self, filename):
        """
        Creates password protected zip file
        :param filename: str
        :return: str
        """
        zip_filename, password = self.get_name_password()
        try:
            with pyzipper.AESZipFile(zip_filename,
                                     'w',
                                     compression=pyzipper.ZIP_LZMA,
                                     encryption=pyzipper.WZ_AES) as zf:
                zf.setpassword(password)
                self.log.info(f'Password protected zip file "{zip_filename}" has been created')
                zf.write(filename)
                self.log.info(f'file "{filename}" has been compressed in "{zip_filename}"')
        except Exception as er:
            self.log.error(sys.exc_info()[:2])
            exit(1)
        return zip_filename, password

    def move_file(self, src_path, dst_path):
        """
        Move files from source to destination
        :param src_path: str
        :param dst_path: str
        :return: None
        """
        shutil.move(src_path, dst_path)
        self.log.info(f'file "{src_path}" is moved to "{dst_path}".')

    def read_zip(self, zip_filename, password):
        """
        Read password protected zip file
        :param zip_filename: str
        :param password: bite
        :return: str
        """
        try:
            with pyzipper.AESZipFile(zip_filename) as zf:
                self.log.info(f'Reading zip file "{zip_filename}"')
                zf.setpassword(password)
                match_obj = re.search(r"filename='([A-Za-z0-9.]+)'", str(zf.infolist()[0]))
                filename = match_obj.group(1)
                file_data = zf.read(filename)
        except Exception as er:
            self.log.error(sys.exc_info()[:2])
            exit(1)
        return filename, file_data

    @staticmethod
    def convert12to24(time_str):
        """
        Converts 12 hour time to 24 hour
        :param time_str: str
        :return: str
        """
        # Checking if last two elements of time
        # is AM and first two elements are 12
        if time_str[-2:] == "AM" and time_str[:2] == "12":
            return "00" + time_str[2:-2]
            # remove the AM
        elif time_str[-2:] == "AM":
            return time_str[:-2]
            # Checking if last two elements of time
        # is PM and first two elements are 12
        elif time_str[-2:] == "PM" and time_str[:2] == "12":
            return time_str[:-2]
        else:
            # add 12 to hours and remove PM
            return str(int(time_str[:2]) + 12) + time_str[2:8]

    def decode_password(self, file_name):
        """
        Decode the password based on fine name
        :param file_name: str
        :return: byte
        """
        # Extract time info from file name
        l1 = file_name.split('_', 3)
        s1 = l1[3].split('.')[0]
        s2 = s1.replace('_', ':')
        s3 = s2.replace(':pm', ' PM') if 'pm' in s2 else s2.replace(':am', ' AM')
        s4 = self.convert12to24(s3)
        l2 = s4.split(':')
        # convert time zone to utc epoch timestamp
        dt = datetime.datetime(int(l1[0]), int(l1[1]), int(l1[2]), int(l2[0]), int(l2[1]), int(l2[2]))
        utc_time = dt.replace(tzinfo=timezone.utc)
        password_utc_timestamp = str(utc_time.timestamp()).split('.')[0].encode('ascii')
        return password_utc_timestamp

    def perform_pii(self, data):
        """
        Perform PII on file path
        e.g.
            for line = "file_path" : "C:\\Users\\john\\xyz", it should be converted to "<d>:\\Users\\<u>\\xyz"
        :param data: list
        :return:list
        """
        pii_filtered = []

        def splitall(path):
            """
            Splits path to all it's path members
            :param path: str
            :return: list
            """
            allparts = []
            while 1:
                parts = os.path.split(path)
                if parts[0] == path:  # sentinel for absolute paths
                    allparts.insert(0, parts[0])
                    break
                elif parts[1] == path:  # sentinel for relative paths
                    allparts.insert(0, parts[1])
                    break
                else:
                    path = parts[0]
                    allparts.insert(0, parts[1])
            return allparts

        # perform PII line by line
        data = data.decode('ascii').split('\n')
        for line in data:
            if line.startswith('"file_path":'):
                line = str(line)
                # separating 'file_path:' string and path string
                l = line.split(':', 1)
                # splitting path
                splited_path = splitall(l[1])
                pii_words = []
                for i in range(len(splited_path)):
                    if ':' in splited_path[i]:
                        pii_words.append(splited_path[i])
                    if splited_path[i] == 'Users':
                        pii_words.append(splited_path[i+1])
                line = line.replace(pii_words[0].split(':')[0] + ':', '<d>:')
                line = line.replace(pii_words[1], '<u>') if len(pii_words) > 1 else line
                pii_filtered.append(line)
            else:
                pii_filtered.append(line)

        self.log.info('Performed PII filtration on file content.')

        return pii_filtered

    def create_pii_filtered_file(self, path, filename, pii_filtered_data):
        """
        Create new file having PII filtered data
        :param path: str
        :param filename: str
        :param pii_filtered_data: list
        :return: None
        """
        filtered_file_name = os.path.join(path, 'PII_filtered_' + filename)
        self.log.info(f'Creating PII_filtered file at : "{filtered_file_name}"')
        with open(filtered_file_name, 'w') as f_obj:
            for line in pii_filtered_data:
                f_obj.write(line)