from email.mime.text import MIMEText
from flask.helpers import url_for
import os
from flask import Flask,render_template,request,redirect,Blueprint,jsonify
from werkzeug.utils import secure_filename
import requests
import json
from datetime import datetime, timezone, timedelta
import locale
# from flask_httpauth import HTTPBasicAuth
app = Flask(__name__, static_folder='static',static_url_path="")
# auth = HTTPBasicAuth()

add_app = Blueprint("datefile", __name__, static_url_path="/drive", static_folder="/mnt/ex-ssd/datefile")#ここのパスも変える
# add_app = Blueprint("datefile", __name__, static_url_path="/drive", static_folder="/home/sumaa/Desktop/api")
app.register_blueprint(add_app)


UPLOAD_FOLDER = '/mnt/ex-ssd/datefile/' #ここに絶対パス
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


wetherapikey = "80efcb09546b956c8fa14024be0cd5fa"

lat = "35.68944"
lon = "139.69167"




# MAIL_ADDRESS = "skotaosugi0219@gmail.com"
# PASSWORD = "kota0219"

# id_list = {
#     "sumaa": "0219",
#     "kanade": "1214",
#     "haruka": "1026"
# }


# @auth.get_password
# def get_pw(id):
#     if id in id_list:
#         return id_list.get(id)
#     return None


# @app.route('/admin')
# @auth.login_required
# def index():
#     return "Hello, %s!" % auth.username()

@app.route(
    "/.well-known"
    "/acme-challenge"
    "/zh4jSTFqq8J7JPU5U1kxob_XhhpXMtP6hy9GqeIAryE")
def acme_challenge():
    return "zh4jSTFqq8J7JPU5U1kxob_XhhpXMtP6hy9GqeIAryE"


@app.route("/")
def hell():
    return render_template("test.html")


@app.route("/GfN")
def GfNindex():
    return render_template("web/GfN.html")

@app.route("/top")
def top():

    return render_template("top.html")

@app.route("/GfN/<string:st>")
def GfN(st):
    s = "web/" + st + ".html"
    return render_template(s)

@app.route("/download")
def download():
    filename = os.listdir(path=app.config['UPLOAD_FOLDER'])
    filekey = list(range(len(filename)))
    return render_template("download.html", data=zip(filename, filekey))


@app.route("/upload")
def upload():
    return render_template("upload.html")


@app.route("/put", methods=["POST"])
def put():
    putFile = request.files["file"]
    putName = secure_filename(putFile.filename)
    putFile.save(os.path.join(app.config['UPLOAD_FOLDER'], putName))
    return jsonify()


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


if __name__ == '__main__':

    


    app.run(host="0.0.0.0",debug=True,threaded=True)
