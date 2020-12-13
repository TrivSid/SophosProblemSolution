** Problem statement **

 Part -1: 
     Create an application that will monitor a specific folder in a system. Once a new .txt (sample attached) file is created/dropped/copied to the folder, 
     application should take the .txt file and create a password protected zip file using the UTC epoch time stamp for the file.
     The name of the zip file should be in the format of YYYY_MM_DD_hh_mm_ss_am/pm.zip (e.g. 2020_08_24_7_24_32_pm.zip)  ( ref: https://www.epochconverter.com/) The password is the UTC time epoch format. 
     The application should drop the zip file into a different folder named "todecode".
      it should create this folder when it is run first time or if the folder is not existing. It should delete any old file (if any exists) in the folder and keep only the new file.

 Part-2:
     Create application that monitors the "todecode" folder for any new zip file.
     When a new file is published, the application should be able to unzip the new zip file.
     The application should be able to identify the password using the file name. 
     Extract file, perform PII filtering, put the contents in the new file (PII_filtered_<original_name>.txt) without any PII information in the file path if the text file has any in the file path.
     if NO PII in the file_path it to display as it is.
     e.g.
     field name to look for is "file_path" : "C:\Users\john\xyz" should be converted to "<d>:\\Users\<u>\xyz"
 
 ** Application Usage **

    -Execute run.py
    -Configure 'monitor' and 'todecode' folder path to config/input.yaml
    -Provide '--part1 on' or '-t on' to track 'monitor' folder or to track '.txt' file in folder
    -Provide '--part2 on' or '-z on' to track 'todecode' folder to track '.zip' file in folder
    -App do not execute both the parts parallel
    -PII performs on the paths provided in '"file_path": <path>"' format
    -App generates log on commandline as well as logs folder
    -Developed on Windows platform, It may work on Linux as well(not tested)