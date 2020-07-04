from flask_cors import CORS, cross_origin
from flask import Flask, jsonify, request, render_template, current_app
from flask import app, safe_join, send_from_directory
import os
import get_trends

app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')
cors = CORS(app)
@app.route("/")
def index():
    trends = get_trends.trends()
    print(trends)
    return render_template('index.html', trend1=trends[0]['name'], trend2=trends[1]['name'], trend3=trends[2]['name'], trend4=trends[3]['name'], trend5=trends[4]['name'], trend6=trends[5]['name'], trend7=trends[6]['name'], trend8=trends[7]['name'], trend9=trends[8]['name'], trend10=trends[9]['name'])
@app.route("/api/<trend_name>")
def get_sentiment(trend_name):
   negPred=get_trends.get_sentiments(trend_name)
   posPred=1-negPred
   return {
            'Negative': negPred, 
            'Positive': posPred
         }   
if __name__ == '__main__':
    app.run(debug=True)
