# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 15:46:24 2020

@author: foryou
"""
import os 
import hashlib
import re
import shutil
from tqdm import tqdm
from Module.FileInformation import FileInformation as fileinformation
from Module import RecordLog

class FileOperator():
    def __init__(self, run_mode, data_path, path):
        self.data_path = data_path
        self.path = path
        self.folder_list = list()
        self.file_list = list()
        self.recordlog = RecordLog.RecordLog(run_mode, path)
        
    def makedirs_create(self, folder):
        sub_path = os.path.join(self.path, folder)
        if not os.path.isdir(sub_path):
            os.makedirs(r'%s/%s' % (self.path, folder))
            
    def sorting_folder(self):
        max_index = 0
        new_folder_list = list()
        for folder in self.folder_list:
            index = re.search("^[0-9]{2}_", os.path.basename(folder))
            
            if index:
                index = index.group(0).replace("_", "")
                new_folder_list.append(os.path.basename(folder))
                if int(index) > max_index:
                    max_index = int(index)
                    
        self.folder_list = new_folder_list
        return max_index
    
    def sorted_reverse(self):
        folder_empty_list = list()
        folder_existed_file_list = list()
        for folder in self.folder_list:
            folder_path = os.path.join(self.path, folder)
            if len(os.listdir(folder_path)) == 0:
                folder_empty_list.append(folder)
            else:
                folder_existed_file_list.append(folder)
        return folder_empty_list, folder_existed_file_list
    
    def fix_index(self, index):
        if len(str(index)) < 2:
            str_index =  "0" + str(index)
        else:
            str_index = str(index)
        return str_index
    
    def remove_refile(self):
        del_list = list()
        for index, file in enumerate(self.file_list):
            for original_file in self.file_list:
                # print(original_file.Path, file.Path)
                # print(original_file.Md5, file.Md5)
                # print(original_file.Date, file.Date)
                if original_file.Path == file.Path:
                    continue
                elif original_file.Md5 == file.Md5:
                    if original_file.Date <= file.Date:
                        shutil.move(file.Path, os.path.join(self.path, "00_delete"))
                        self.recordlog.write_classified_log(original_file, file)
                        del_list.append(self.file_list.index(file))
                        break
                    
        for add, index in enumerate(del_list):
            del self.file_list[index-add]
                    
    def classified_file(self, folder_index):
        folder_index = folder_index + 1
        
        for index, file in enumerate(self.file_list):
            folder_exist = fileinformation.get_folder_exist(self.folder_list[1:], file)
            if folder_exist:
                shutil.move(file.Path, os.path.join(self.path, folder_exist))
            else:
                folder_name = self.fix_index(folder_index) + "_" + file.Filename_extension
                self.makedirs_create(folder_name)
                shutil.move(file.Path, os.path.join(self.path, folder_name))
                folder_index = folder_index + 1
                self.folder_list.append(folder_name)
                
    def reversed_file(self):
        for folder in self.folder_list:
            if not folder == "00_Organize_logs":
                print(folder + " ok")
                folder_path = os.path.join(self.path, folder)
                for file in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, file)
                    shutil.move(file_path, self.data_path)
            else:
                continue
        