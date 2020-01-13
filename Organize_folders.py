# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 16:36:20 2020

@author: foryou
"""

import os 
import hashlib
import time
import shutil
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
    
def start_log(path, run_mode):
    log_path = os.path.join(path, "00_Organize_logs")
    with open(os.path.join(log_path, "delete.log"), 'a') as f:
        f.write(time.strftime(r"%Y-%m-%d_%H-%M-%S", time.localtime()) + " -> " + run_mode + "\n\n")
        
def write_classified_log(path, original_file, file):
    log_path = os.path.join(path, "00_Organize_logs")
    with open(os.path.join(log_path, "delete.log"), 'a') as f:
        f.write("+" + original_file.Path + " -> -" + file.Path + "\n")
        f.write("md5 : " + original_file.Md5 + " -> " + file.Md5 + "\n\n")
        
def write_reversed_log(path, folder_empty_list, folder_existed_file_list):
    log_path = os.path.join(path, "00_Organize_logs")
    with open(os.path.join(log_path, "delete.log"), 'a') as f:
        f.write(str(folder_empty_list) + " -> Number of files = 0 \n\n")
        f.write(str(folder_existed_file_list) + " ->  Number of files > 0 \n\n")

def makedirs_create(path, folder):
    sub_path = os.path.join(path, folder)
    if not os.path.isdir(sub_path):
        os.makedirs(r'%s/%s' % (path, folder))
        
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
            
            file = File(path_file)
            file_list.append(file)
            pbar.update(1)
        
    return file_list, folder_list

def sorting_folder(folder_list):
    max_index = 0
    new_folder_list = list()
    for folder in folder_list:
        index = re.search("^[0-9]{2}_", os.path.basename(folder))
        
        if index:
            index = index.group(0).replace("_", "")
            new_folder_list.append(os.path.basename(folder))
            if int(index) > max_index:
                max_index = int(index)
    
    return max_index, new_folder_list

def fix_index(index):
    if len(str(index)) < 2:
        str_index =  "0" + str(index)
    else:
        str_index = str(index)
    return str_index

def get_folder_exist(folder_list, file):
    for folder in folder_list:
        if file.Filename_extension in folder:
            return folder

def remove_refile(file_list, path):
    del_list = list()
    for index, file in enumerate(file_list):
        for original_file in file_list:
            # print(original_file.Path, file.Path)
            # print(original_file.Md5, file.Md5)
            # print(original_file.Date, file.Date)
            if original_file.Path == file.Path:
                continue
            elif original_file.Md5 == file.Md5:
                if original_file.Date <= file.Date:
                    shutil.move(file.Path, os.path.join(path, "00_delete"))
                    write_classified_log(path, original_file, file)
                    del_list.append(file_list.index(file))
                    break
                
    for add, index in enumerate(del_list):
        del file_list[index-add]
        
    return file_list
                
def classified_file(file_list, folder_list, folder_index, path):
    folder_index = folder_index + 1
    
    for index, file in enumerate(file_list):
        folder_exist = get_folder_exist(folder_list[1:], file)
        if folder_exist:
            shutil.move(file.Path, os.path.join(path, folder_exist))
        else:
            folder_name = fix_index(folder_index) + "_" + file.Filename_extension
            makedirs_create(path, folder_name)
            shutil.move(file.Path, os.path.join(path, folder_name))
            folder_index = folder_index + 1
            folder_list.append(folder_name)
            
def reversed_file(folder_list, path, data_path):
    for folder in folder_list:
        if not folder == "00_Organize_logs":
            print(folder + " ok")
            folder_path = os.path.join(path, folder)
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                shutil.move(file_path, data_path)
        else:
            continue
        
def sorted_reverse_log(folder_list, path):
    folder_empty_list = list()
    folder_existed_file_list = list()
    for folder in folder_list:
        folder_path = os.path.join(path, folder)
        if len(os.listdir(folder_path)) == 0:
            folder_empty_list.append(folder)
        else:
            folder_existed_file_list.append(folder)
    
    write_reversed_log(path, folder_empty_list, folder_existed_file_list)
    
if __name__ == "__main__":
    data_path = r'D:\Download'
    print("Data mode : 1.Classification, 2.Reverse")
    run_mode = input('請輸入您要使用的模式:\n') or "Classification"
    path = os.path.join(data_path, "00_Organize_folders")#data_path
    makedirs_create(path, "00_delete")
    makedirs_create(path, "00_Organize_logs")
    start_log(path, run_mode)
    file_list, folder_list = get_file_list(run_mode, path, data_path)
    index, folder_list = sorting_folder(folder_list)
    
    if run_mode == "Classification":
        file_list = remove_refile(file_list, path)
        classified_file(file_list, folder_list, index, path)
    elif  run_mode == "Reverse":
        reversed_file(folder_list, path, data_path)
        sorted_reverse_log(folder_list, path)