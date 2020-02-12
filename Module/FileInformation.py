# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 16:32:29 2020

@author: foryou
"""
import os 
import hashlib
import re
from tqdm import tqdm

class File():
    def __init__(self, path):
        self.Path = path
        self.Md5 = self.get_md5(path)
        self.Date = os.path.getctime(path)
        self.Filename_extension = path.split('.')[-1].lower()
        
    def get_md5(self, filename):
        with open(filename, 'rb') as file:
            data = file.read()
            hash_md5 = hashlib.md5(data).hexdigest()
        return hash_md5

class FileInformation():
    def get_file_list(run_mode, path, data_path):
        if run_mode == "Reverse":
            data_path = path
        file_list = list()
        folder_list = list()
        with tqdm(total = len(os.listdir(data_path)), desc = "Search file", leave = False) as pbar:  
            for file in os.listdir(data_path):
                path_file = os.path.join(data_path, file)
                if os.path.isdir(path_file):
                    folder_list.append(path_file)
                    pbar.update(1)
                    continue
                
                file_module = File(path_file)
                file_list.append(file_module)
                pbar.update(1)
            
        return file_list, folder_list
    
    def get_folder_exist(folder_list, file):
        for folder in folder_list:
            if file.Filename_extension in folder:
                return folder
        