from flask import Flask ,request,redirect,url_for,render_template

app = Flask( __name__ ) 

@app.route('/') 
def hello_world():

    return render_template('test.html')

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=13700, debug=True)