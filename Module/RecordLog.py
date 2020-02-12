# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 16:19:34 2020

@author: foryou
"""

import os 
import time

class RecordLog():
    def __init__(self, run_mode, path):
        self.run_mode = run_mode
        self.log_path = os.path.join(path, "00_Organize_logs")
        
    def start_log(self):
        with open(os.path.join(self.log_path, "delete.log"), 'a') as f:
            f.write(time.strftime(r"%Y-%m-%d_%H-%M-%S", time.localtime()) + " -> " + self.run_mode + "\n\n")
            
    def write_classified_log(self, original_file, file):
        with open(os.path.join(self.log_path, "delete.log"), 'a') as f:
            f.write("+" + original_file.Path + " -> -" + file.Path + "\n")
            f.write("md5 : " + original_file.Md5 + " -> " + file.Md5 + "\n\n")
            
    def write_reversed_log(self, folder_empty_list, folder_existed_file_list):
        with open(os.path.join(self.log_path, "delete.log"), 'a') as f:
            f.write(str(folder_empty_list) + " -> Number of files = 0 \n\n")
            f.write(str(folder_existed_file_list) + " ->  Number of files > 0 \n\n")
            