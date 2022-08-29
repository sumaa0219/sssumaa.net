import numpy as np
import pandas as pd
import requests
import json
from datetime import datetime, timezone, timedelta
import locale

wetherapikey = "80efcb09546b956c8fa14024be0cd5fa"

class apiX:
    def __init__(self):
        global df
        df = pd.read_csv("/home/sumaa/Desktop/api/static/date/ApiDateBase.csv",index_col=0)
        pass

    def wheather(self, lat, lon):
        reswea = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=" + lat + "&lon="+lon +"&exclude=dairy&appid="+wetherapikey+"&lang=ja&units=metric")
        return json.dumps(reswea.json())

    def convtime(self, unixtime):
        JST = timezone(timedelta(hours=+9), 'JST')
        dt = datetime.fromtimestamp(unixtime).replace(tzinfo=timezone.utc).astimezone(tz=JST)
        locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
        date = dt.strftime('%a')
        return  str(date)
    
    def unixJST(self, time):
        JST = timezone(timedelta(hours=+9), 'JST')
        dt = datetime.fromtimestamp(time).replace(tzinfo=timezone.utc).astimezone(tz=JST)
        locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
        return dt.strftime('%Y/%m/%d %H:%M:%S')

    def GetStatus(self, element):
        value = 0
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
        return "Post_Succese"
    
    def GetSetting(self, element):
        value = 0
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
