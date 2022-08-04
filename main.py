from crypt import methods
from email.mime.text import MIMEText
from itertools import count
from re import template
from tkinter import E
from flask.helpers import url_for
from flask_httpauth import HTTPBasicAuth
import csv
import os
import os.path
from flask import Flask,render_template,request,redirect,Blueprint,jsonify
import numpy as np
from werkzeug.utils import secure_filename
import requests
import json
from datetime import datetime, timezone, timedelta
import locale
import psutil 
from multiprocessing import Process
import pandas as pd
import api

app = Flask(__name__, static_folder='static',static_url_path="")
auth = HTTPBasicAuth()

add_app = Blueprint("datefile", __name__, static_url_path="/drive", static_folder="/mnt/ex-ssd/datefile")#ここのパスも変える
# add_app = Blueprint("datefile", __name__, static_url_path="/drive", static_folder="/home/sumaa/Desktop/api")
app.register_blueprint(add_app)


UPLOAD_FOLDER = '/mnt/ex-ssd/datefile/' #ここに絶対パス
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_AS_ASCII'] = False


wetherapikey = "80efcb09546b956c8fa14024be0cd5fa"

lat = "42.2128"
lon = "-71.0342"

users = {
    "sumaa": "kota0219",
    "admin": "skotakota0219"
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/.well-known/acme-challenge/<filename>')
def well_known(filename):
    return render_template('.well-known/acme-challenge/'+ filename)


@app.route("/")
def test():
    return render_template("test.html")


@app.route("/top")
def top():
    number=[1,2,3,4,5,6]
    name=[]
    date=[]
    csv_file = open("/home/sumaa/Desktop/api/static/date/favorite.csv", "r", encoding="UTF-8", errors="", newline="" )
    f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

    for row in f:
        name.append(row[0])
        date.append(row[1])
        print(row)

    return render_template("top.html",data=zip(number,name,date))

@app.route("/download")
def download():
    list_ext=[]
    list_size=[]
    list_date=[]
    filename = os.listdir(path=app.config['UPLOAD_FOLDER'])
    filename.sort()
    count=len(filename)
    for x in range(count):
        ext = filename[x].find('.')
        size = os.path.getsize(UPLOAD_FOLDER + filename[x])
        time = os.path.getctime(UPLOAD_FOLDER + filename[x])
        list_ext.append(filename[x][ext+1:].lower())

        if size >= 1000000000000:
            size = size/1000000000000
            sizeB =str(size)+"TB"

        elif size >= 1000000000:
            size = size/1000000000
            sizeB =str(size)+"GB"

        elif size >= 1000000:
            size = size/1000000
            sizeB =str(size)+"MB"

        elif size >= 1000:
            size = size/1000
            sizeB =str(size)+"KB"

        else:
            sizeB =str(size)+"B"

        list_date.append(unixJST(time))
        list_size.append(sizeB)

    filekey = list(range(len(filename)))
    return render_template("download.html", data=zip(filename, list_ext,list_size,list_date, filekey))


@app.route("/upload")
def upload():
    return render_template("upload.html")


@app.route("/put", methods=["POST"])
def put():
    putFile = request.files["file"]
    putName = secure_filename(putFile.filename)
    putFile.save(os.path.join(app.config['UPLOAD_FOLDER'], putName))
    return jsonify()

@app.route("/register", methods=["POST"])
def register():
    favorite=[]
    regiword: str = request.form["word"]
    reginame: str = request.form["name"]
    regiID: int = request.form["id"]
    ID= int(regiID)-1
    print(reginame)
    print(regiword)
    csv_file = open("/home/sumaa/Desktop/api/static/date/favorite.csv", "r", encoding="UTF-8", errors="", newline="" )
    f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)


    count = 0
    for row in f:
        if ID == count:
            favorite.append([reginame,regiword])
        else:
            favorite.append(row)
        count += 1

    csv_file.close()


    e = open("/home/sumaa/Desktop/api/static/date/favorite.csv", mode="w", newline="")
    writer = csv.writer(e)
    for data in favorite:
        writer.writerow(data)
    e.close()

    return jsonify()


@app.route("/editfavo")
@auth.login_required
def edit():
    number=[1,2,3,4,5,6]
    name=[]
    date=[]
    csv_file = open("/home/sumaa/Desktop/api/static/date/favorite.csv", "r", encoding="UTF-8", errors="", newline="" )
    f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

    for row in f:
        name.append(row[0])
        date.append(row[1])
        print(row)

    return render_template("favorite.html",data=zip(number,name,date))



@app.route("/delete/<filename>", methods=["POST"])
def delete(filename):
    os.remove(app.config['UPLOAD_FOLDER'] + str(filename))
    print(filename)
    return jsonify()

@app.route("/youtube")
def youtube():
    return render_template("youtube.html")

@app.route("/wheather")
def wheather():
    params = {'zipcode':'2330008'}
    reswea = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=" + lat + "&lon="+lon +"&exclude=dairy&appid="+wetherapikey+"&lang=ja&units=metric", params=params)
    return json.dumps(reswea.json())
    
@app.route("/unixJST/<int:unixtime>")
def convtime(unixtime):
    JST = timezone(timedelta(hours=+9), 'JST')
    dt = datetime.fromtimestamp(unixtime).replace(tzinfo=timezone.utc).astimezone(tz=JST)
    locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
    date = dt.strftime('%a')
    return  str(date)

@app.route("/disk-info")
def diskinfo():
    dsk = psutil.disk_usage('/mnt/ex-ssd/datefile')
    return str(dsk.percent)


def unixJST(time):
    JST = timezone(timedelta(hours=+9), 'JST')
    dt = datetime.fromtimestamp(time).replace(tzinfo=timezone.utc).astimezone(tz=JST)
    locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')

    return dt.strftime('%Y/%m/%d %H:%M:%S')


@app.route("/api/<string:type>")
def api(type):
    api_Element = request.args.get("element", type=str)
    api_Type = request.args.get("type", type=str)
    api_Value = request.args.get("value",type=int)
    api = api.api()
    
    if type == "status":
        if api_Type == "R" or api_Type == "r":
            return api.GetStatus(api_Element)

        elif api_Type == "W" or api_Type == "w":
            return api.PostStatus(api_Element,api_Value)

    elif type == "setting":
        if api_Type == "R" or api_Type == "r":
            return api.GetSetting(api_Element)

        elif api_Type == "W" or api_Type == "w":
            return api.PostSetting(api_Element,api_Value)

@app.route("/try")
def ty():

    api = api.api()
    return api.GetStatus(element="tempreture")



if __name__ == '__main__':


    app.run(host="0.0.0.0",ssl_context=('/etc/letsencrypt/live/sssumaa.net/fullchain.pem', '/etc/letsencrypt/live/sssumaa.net/privkey.pem'),debug=True,threaded=True)


# sumaa@raspberrypi:~/Desktop/api $ sudo certbot certonly --webroot -w /home/sumaa/Desktop/api/templates/ -d sssumaa.net