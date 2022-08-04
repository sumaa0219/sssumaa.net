from pickletools import int4
import numpy as np
import pandas as pd


class api:
    def __init__(self):
        global df
        df = pd.read_csv("/home/sumaa/Desktop/api/static/date/ApiDateBase.csv",index_col=0)
        pass

    def GetStatus(self, element):
        self.element = element
        id = "status"
        value = df[id][self.element]
        return value

    def PostStatus(self, element, value:int):
        self.element = element
        self.value:int = value
        id = "status"
        df.at[self.element,id] = self.value
        df.to_csv("/home/sumaa/Desktop/api/static/date/ApiDateBase.csv")
        return "Post_Status"
    
    def GetSetting(self, element):
        self.element = element
        id = "setting"
        value = df[id][self.element]
        return value

    def PostSetting(self, element, value:int):
        self.element = element
        self.value:int = value
        id = "setting"
        df.at[self.element,id] = self.value
        df.to_csv("/home/sumaa/Desktop/api/static/date/ApiDateBase.csv")
        return "Post_setting"
