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

class File():
    def __init__(self, path):
        self.Path = path
        self.Md5 = self.get_md5(path)
        self.Date = os.path.getctime(path)
        self.Filename_extension = path.split('.')[-1].lower()
        
    def get_md5(self, filename):
        m = hashlib.md5()
        with open(filename, 'rb') as file:
            data = file.read()
            hash_md5 = hashlib.md5(data).hexdigest()
        return hash_md5
    
def write_log(path, original_file, file):
    log_path = os.path.join(path, "00_Organize_folders")
    with open(os.path.join(log_path, "delete.log"), 'a') as f:
        f.write("+" + original_file.Path + " -> -" + file.Path + "\n")
        f.write("md5 : " + original_file.Md5 + " -> " + file.Md5 + "\n\n")

def makedirs_create(path, folder):
    sub_path = os.path.join(path, folder)
    if not os.path.isdir(sub_path):
        os.makedirs(r'%s/%s' % (path, folder))
        
def get_file_list(path):
    file_list = list()
    folder_list = list()
    for file in os.listdir(path):
        path_file = os.path.join(path, file)
        if os.path.isdir(path_file):
            folder_list.append(path_file)
            continue
        
        file = File(path_file)
        file_list.append(file)
        
    return file_list, folder_list

def search_folder_index(folder_list):
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
        for original_file in file_list[index:]:
            if original_file.Path == file.Path:
                continue
            elif original_file.Md5 == file.Md5:
                if original_file.Date <= file.Date:
                    shutil.move(file.Path, os.path.join(path, "00_delete"))
                    write_log(path, original_file, file)
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
        
    
if __name__ == "__main__":
    path = r'D:\download'
    makedirs_create(path, "00_delete")
    makedirs_create(path, "00_Organize_folders")
    file_list, folder_list = get_file_list(path)
    file_list = remove_refile(file_list, path)
    index, folder_list = search_folder_index(folder_list)
    classified_file(file_list, folder_list, index, path)