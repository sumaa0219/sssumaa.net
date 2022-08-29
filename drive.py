from csv import list_dialects
from inspect import Parameter
import os
from tkinter import E
from turtle import Turtle
import api

BasePath ="/mnt/ex-ssd/datefile/"
BaseURL = "https://sssumaa.net"
apixx=api.apiX()

class driveX:
    def __init__(self):
        
        return None

    def show(self, path):
        global DrivePath
        self.path = path
        DrivePath = BasePath + self.path
        filename = os.listdir(path=DrivePath)
        return filename

    def sort(self, path, SortType="sort"):
        self.path = path
        SortList=drive.show(self.path)
        self.count=len(SortList)
        if SortType == "sort":
            SortList.sort()

        elif SortType == "unsort":
            SortList.sort(reverse=True)

        return SortList

    def info(self, Listx:list, point):
        self.List = Listx
        FilePath = DrivePath + self.List[point]
        self.size = drive.Bite(os.path.getsize(FilePath))
        self.time = apixx.unixJST(os.path.getctime(FilePath))
        ext = self.List[point].find('.')
        self.ext = self.List[point][ext+1:].lower()
    
        return [self.size, self.time, self.ext]

        

    def Bite(self, size):
        self.size=size
        if self.size >= 1000000000000:
            self.size = self.size/1000000000000
            return str(self.size)+"TB"

        elif self.size >= 1000000000:
            self.size = self.size/1000000000
            return str(self.size)+"GB"

        elif self.size >= 1000000:
            self.size = self.size/1000000
            return str(self.size)+"MB"

        elif self.size >= 1000:
            self.size = self.size/1000
            return str(self.size)+"KB"

        else:
            return str(self.size)+"B"

    def GenerateURL(self, List:list,RootPath):
        self.List = List
        self.RootPath = RootPath
        URLList = []
        for i in range(len(self.List)):
            SerchPath = DrivePath + self.List[i]
            idx = SerchPath.find(BasePath)
            FilePath = SerchPath[idx+len(BasePath):]

            if os.path.isdir(SerchPath) == True:
                URL = self.RootPath + "?path=" + FilePath
                #print(SerchPath + " " + self.RootPath + " " + FilePath)

            else:
                URL = "/drive/" + FilePath
            
            URLList.append(URL)

        return URLList

    def PathList(self,path,url):
        self.path = path
        self.url = url
        pathlist = self.path.split("/")
        PathURLList = []
        PathName = []

        for i in range(len(pathlist)):
            if i == 0:
                pathxx = pathlist[i]
            else:
                pathxx = pathxx + "/" + pathlist[i]
            PathName.append(pathlist[i])
            PathURLList.append(BaseURL + self.url +"?path="+ pathxx)
        return range(len(pathlist)),PathName,PathURLList
drive=driveX()