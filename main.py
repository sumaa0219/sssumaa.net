from code import interact
from crypt import methods
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
import psutil 
import api
from flask_login import UserMixin,LoginManager,login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__, static_folder='static',static_url_path="")
auth = HTTPBasicAuth()

global URL

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = os.urandom(24)
class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), nullable=False, unique=True)
	password = db.Column(db.String(25))

add_app = Blueprint("datefile", __name__, static_url_path="/drive", static_folder="/mnt/ex-ssd/datefile")#ここのパスも変える
# add_app = Blueprint("datefile", __name__, static_url_path="/drive", static_folder="/home/sumaa/Desktop/api")
app.register_blueprint(add_app)


UPLOAD_FOLDER = '/mnt/ex-ssd/datefile/' #ここに絶対パス
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_AS_ASCII'] = False

apixx = api.apiX()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        # Userのインスタンスを作成
        user = User(username=username, password=generate_password_hash(password, method='sha256'))
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        # Userテーブルからusernameに一致するユーザを取得
        user = User.query.filter_by(username=username).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect('/top')
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.errorhandler(401)
def page_not_found(e):
    print(e)
    return redirect('/login')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/.well-known/acme-challenge/<filename>')
def well_known(filename):
    return render_template('.well-known/acme-challenge/'+ filename)


@app.route("/top")
@login_required
def test():
    print(current_user.id)
    return render_template("top.html")


@app.route("/")
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

    return render_template("index.html",data=zip(number,name,date))

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

        list_date.append(apixx.unixJST(time))
        list_size.append(sizeB)

    filekey = list(range(len(filename)))
    return render_template("download.html", data=zip(filename, list_ext,list_size,list_date, filekey))


@app.route("/upload")
@login_required
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
def edit():
    number=[1,2,3,4,5,6]
    name=[]
    date=[]
    csv_file = open("/home/sumaa/Desktop/api/static/date/favorite.csv", "r", encoding="UTF-8", errors="", newline="" )
    f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

    for row in f:
        name.append(row[0])
        date.append(row[1])

    return render_template("favorite.html",data=zip(number,name,date))



@app.route("/delete/<filename>", methods=["POST"])
def delete(filename):
    os.remove(app.config['UPLOAD_FOLDER'] + str(filename))
    print(filename)
    return jsonify()

@app.route("/disk-info")
def diskinfo():
    dsk = psutil.disk_usage('/mnt/ex-ssd/datefile')
    return str(dsk.percent)

@app.route("/api/<string:type>")
def api(type):
    api_Element = request.args.get("element", type=str)
    api_Type = request.args.get("type", type=str)
    api_Value = request.args.get("value",type=int)
    api_lat = request.args.get("lat",type=str)
    api_lon = request.args.get("lon",type=str)
    api_unixtime = request.args.get("unixtime",type=int)
    
    if type == "status":
        if api_Type == "R" or api_Type == "r":
            return apixx.GetStatus(api_Element)

        elif api_Type == "W" or api_Type == "w":
            return apixx.PostStatus(api_Element,api_Value)

    elif type == "setting":
        if api_Type == "R" or api_Type == "r":
            return apixx.GetSetting(api_Element)

        elif api_Type == "W" or api_Type == "w":
            return apixx.PostSetting(api_Element,api_Value)
    
    elif type == "wheather":
        return apixx.wheather(api_lat,api_lon)
    
    elif type == "unixJST":
        return apixx.convtime(api_unixtime)


@app.route("/try")
def ty():

    api = api.api()
    return api.GetStatus(element="tempreture")



if __name__ == '__main__':


    app.run(host="0.0.0.0",ssl_context=('/etc/letsencrypt/live/sssumaa.net/fullchain.pem', '/etc/letsencrypt/live/sssumaa.net/privkey.pem'),debug=True,threaded=True)


# sumaa@raspberrypi:~/Desktop/api $ sudo certbot certonly --webroot -w /home/sumaa/Desktop/api/templates/ -d sssumaa.net