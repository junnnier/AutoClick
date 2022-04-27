# -*- coding: utf-8 -*-
import csv

class ExecuteData(object):
    def __init__(self):
        self.data=list()

    def add_data(self,info):
        self.data.append(info)

    def insert_data(self,index,info):
        self.data.insert(index,info)

    def remove_data(self,index):
        self.data.pop(index)

    def remove_all_data(self):
        self.data=list()

    def save_data(self,save_path):
        with open(save_path,"w",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(self.data)

    def load_data(self,file_path):
        with open(file_path,"r",encoding="utf-8") as f:
            reader = csv.reader(f)
            self.data=list(reader)

db=ExecuteData()