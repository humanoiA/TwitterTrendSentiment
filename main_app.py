from flask_cors import CORS, cross_origin
from flask import Flask, jsonify, request, render_template, current_app, session
from flask import app, safe_join, send_from_directory
import os
import get_trends
from flask_pymongo import PyMongo
import bcrypt
app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')
app.config['MONGO_DBNAME'] = 'userLogin'
app.config['MONGO_URI'] = 'mongodb+srv://humanoid:4v4dMl1YiqoKoB0A@cluster0.smoja.mongodb.net/kofta?retryWrites=true&w=majority'
app.config['SECRET_KEY'] = 'kjhVHTY%^$%RV76BH#$i8'  
mongo = PyMongo(app)
cors = CORS(app)
@app.route("/")
def index():
    if 'username' in session:
        trends = get_trends.trends()
        print(trends)
        return render_template('index.html', trend1=trends[0]['name'], trend2=trends[1]['name'], trend3=trends[2]['name'], trend4=trends[3]['name'], trend5=trends[4]['name'], trend6=trends[5]['name'], trend7=trends[6]['name'], trend8=trends[7]['name'], trend9=trends[8]['name'], trend10=trends[9]['name'],user=session['username'])
    return login()
@app.route("/api/<trend_name>")
def get_sentiment(trend_name):
   negPred=get_trends.get_sentiments(trend_name)
   posPred=1-negPred
   return {
            'Negative': negPred, 
            'Positive': posPred
         }   
'''@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return index()
    return render_template('login.html', error=error)'''
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        users = mongo.db['userLogin']
        login_user = users.find_one({'name' : request.form['username']})

        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
                session['username'] = request.form['username']
                return index()

        return 'Invalid username/password combination'
    return render_template('login.html')
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db['userLogin']
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            hashpass = hashpass.decode("utf8")
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return index()
        
        return 'That username already exists!'

    return render_template('register.html')
if __name__ == '__main__':
    app.run(debug=True)
