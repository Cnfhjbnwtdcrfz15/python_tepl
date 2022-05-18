try:
  from flask import Flask, render_template, send_from_directory,json, Response,request
except ModuleNotFoundError:
  import pip
  pip.main(['install','flask'])
  from flask import Flask, render_template, send_from_directory,json, Response,request

import configparser
import numpy as np
import requests
from camera import Camera

camera = Camera()
config = configparser.ConfigParser()
app = Flask(__name__)

@app.route('/', methods=['GET'])
def getdata():
    error = None
    air_temp = request.args.get('temp')
    air_hum = request.args.get('air')
    config.read('123.ini')
    print(f"temp={air_temp}  hum={air_hum}")
    svet = config['PARAM']['svet']
    pomp = config['PARAM']['pomp']
    vent = config['PARAM']['vent']
    temp = config['PARAM']['temp']
    h_a = config['PARAM']['hum_air']
    h_p = config['PARAM']['hum_pos']
    return f"Svet - {svet} Pompa - {pomp} Vent - {vent}; Temp - {temp} air hudmiti - {h_a} soil hudmiti - {h_p}"
    
@app.route('/', methods=['POST'])
def getdatapost():
    error = None
    temp = request.args.get('temp')
    if temp and temp != '':
        print(f"temp={temp}")
        return temp
    else:
        error = 'Не введен запрос!'
        print('error')
        return 'error'

@app.route("/")
def entrypoint():
	return render_template("index.html")

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
			   b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')

@app.route("/cam")
def video_feed():
	return Response(gen(camera),
		mimetype="multipart/x-mixed-replace; boundary=frame")

app.run(host='0.0.0.0',port=80)
