# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 15:46:24 2020

@author: foryou
"""
import os 
import re
import shutil
from Module.FileInformation import FileInformation as fileinformation
from Module import RecordLog

class FileOperator():
    def __init__(self, run_mode, data_path, path):
        self.data_path = data_path
        self.path = path
        self.folder_list = list()
        self.file_list = list()
        self.comparison_list = list()
        self.run_mode = run_mode
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
    
    def is_integer(self, n):
        try:
            int(n)
        except ValueError:
            return False
        return n
    
    def exist_file_rename(self, file, target_path):
        new_file = os.path.join(target_path, os.path.basename(file.Path))
        
        exist = False
        while(os.path.isfile(new_file)):
            index = re.search("\(.*\)", os.path.basename(new_file))
            if index and self.is_integer( index.group(0).strip("(").strip(")") ):
                index = int( index.group(0).strip("(").strip(")") ) + 1
                new_file = re.sub("\(.*\)", "(" + str( index ) + ")", new_file)
                exist = True 
            else:
                new_file = new_file.split(".")[0] + " (1)." + new_file.split(".")[1]
                exist = True
            
        return exist, new_file
    
    def move_file(self, file, file_path):
        exist, new_file = self.exist_file_rename(file, file_path)
        if exist:
            os.rename(file.Path, new_file)   
        else:
            shutil.move(file.Path, file_path)
    
    def remove_refile(self):
        if not self.run_mode == "Comparison":  
            self.comparison_list = self.file_list
            del_list = list()
            
        for index, file in enumerate(self.comparison_list):
            for original_file in self.file_list:
                # print(original_file.Path, file.Path)
                # print(original_file.Md5, file.Md5)
                # print(original_file.Date, file.Date)
                if original_file.Path == file.Path:
                    continue
                elif original_file.Md5 == file.Md5:
                    if original_file.Date <= file.Date:
                        self.recordlog.write_repeated_log(original_file, file)
                        
                        delete_path = os.path.join(self.path, "00_delete")
                        self.move_file(file, delete_path)
                        
                        if not self.run_mode == "Comparison":  
                            del_list.append(self.file_list.index(file))
                        break
                    
                    elif self.run_mode == "Comparison":
                        self.recordlog.write_repeated_log(file, original_file)
                        
                        delete_path = os.path.join(self.path, "00_delete")
                        self.move_file(original_file, delete_path)
                        break
                    
        if not self.run_mode == "Comparison":  
            for add, index in enumerate(del_list):
                del self.file_list[index-add] 
                   
    def classified_file(self, folder_index):
        folder_index = folder_index + 1
        for index, file in enumerate(self.file_list):
            folder_exist = fileinformation.get_folder_exist(self.path, self.folder_list[1:], file)
            if folder_exist:
                self.move_file(file, os.path.join(self.path, folder_exist))
            else:
                folder_name = self.fix_index(folder_index) + "_" + file.Filename_extension
                self.makedirs_create(folder_name)
                
                folder_path = os.path.join(self.path, folder_name)
                self.move_file(file, folder_path)
                    
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
        