# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 16:36:20 2020

@author: foryou
"""

import os 
from Module import FileOperator, RecordLog
from Module.FileInformation import FileInformation as fileinformation

class OrganizeFolders():
    def __init__(self, run_mode, data_path):
        self.run_mode = run_mode 
        self.data_path = data_path
        self.path = os.path.join(data_path, "00_Organize_folders")
        self.index = 0
        self.fileoperator = FileOperator.FileOperator(run_mode, data_path, self.path)
        self.recordlog = RecordLog.RecordLog(run_mode, self.path)
        self.start()
    
    def start(self):
        self.fileoperator.makedirs_create("00_delete")
        self.fileoperator.makedirs_create("00_Organize_logs")
        self.recordlog.start_log()
        
        file_list, folder_list = fileinformation.get_file_list(self.run_mode, self.path, self.data_path)
        self.fileoperator.file_list = file_list
        self.fileoperator.folder_list = folder_list
        
        self.index = self.fileoperator.sorting_folder()
        
    def compared_mode(self, comparison_path):
        file_list, folder_list = fileinformation.get_file_list(self.run_mode, self.path, comparison_path)
        self.fileoperator.comparison_list = file_list
        self.fileoperator.remove_refile()
        
    def classified_mode(self):
        self.fileoperator.remove_refile()
        self.fileoperator.classified_file(self.index)
        
    def reversed_mode(self):
        self.fileoperator.reversed_file()
        folder_empty_list, folder_existed_file_list = self.fileoperator.sorted_reverse()
        self.recordlog.write_reversed_log(folder_empty_list, folder_existed_file_list)

def main(run_mode, data_path, comparison_path):
    organizefolders = OrganizeFolders(run_mode, data_path)
    if run_mode == "Classification":
        organizefolders.classified_mode()
    elif  run_mode == "Reverse":
        organizefolders.reversed_mode()
    elif run_mode == "Comparison":
        organizefolders.compared_mode(comparison_path)
    
if __name__ == "__main__":
    data_path = r'D:\download'
    comparison_path = r'D:\test'
    print("Data mode : 1.Classification, 2.Reverse 3.Comparison")
    run_mode = input('請輸入您要使用的模式:\n') or "Classification"
    if run_mode == "1":
        run_mode = "Classification"
    elif run_mode == "2":
        run_mode = "Reverse"
    elif run_mode == "3":
        run_mode = "Comparison"
    
    main(run_mode, data_path, comparison_path)
