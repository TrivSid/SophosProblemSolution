"""
===============================================================================================
Python Version : 3.6 and above
Date           : 13-12-202
Author         : Siddharth Trivedi
Contact        : iamsidtrivedi@gmail.com, 8320957854
APP USAGE      :
                 Execute run.py
                 Configure 'monitor' and 'todecode' folder path to config/input.yaml
                 Provide '--part1 on' or '-t on' to track 'monitor' folder to track '.txt' file in folder
                 Provide '--part2 on' or '-z on' to track 'todecode' folder to track '.zip' file in folder
                 Application do not execute both the parts in parallel.
                 If needed, execute run.py on different command window with repective command line argument
                 PII performs only on those paths which follows "file_path": <path>"' format
                 Application generates log on commandline as well as logs folder
                 Developed on Windows platform, It may work on Linux as well(not tested)
=================================================================================================
"""
from main import Main

if __name__ == '__main__':
    Main().main()
