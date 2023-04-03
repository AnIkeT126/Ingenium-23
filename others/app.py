import time
from flask import Flask, render_template, request
import requests
import RPi.GPIO as GPIO
import soil
import time

GPIO.setup(17, GPIO.IN)
GPIO.setup(18, GPIO.IN)
GPIO.setup(21, GPIO.OUT)

moisture_value_1 = GPIO.input(17)
moisture_value_2 = GPIO.input(18)

access_key = "2fc00c5a-1ca4-4744-91a7-f89c97c76d7a"

app = Flask(__name__, template_folder='template')

# home page route
@app.route('/')
def index():
    return render_template('irri.html')

# watering page route
@app.route('/watering', methods=['GET', 'POST'])
def watering():
    if request.method == 'POST':
        lat = request.form['lat']
        lng = request.form['lon']
        lats = str(lat)
        lngs = str(lng)
        headers = {
            "X-Meteum-API-Key": access_key
        }
        query = """{
            weatherByPoint(request: { lat:""" + lats + """, lon: """ + lngs+""" }) {
                now {
                        temperature
                        precType
                        precStrength
                    }
                }
            }"""

        response = requests.post('https://api.meteum.ai/graphql/query', headers=headers, json={'query': query})
        r = response.json()
        precp = "ZERO"
        for d in r.values():
            for j in d['weatherByPoint'].values():
                precp = j['precStrength']
        
        
        msg = "random"
        """

        if ((precp== "WEAK" or precp== "MODERATE" or precp== "ZERO") and (soil.moisture_value_1 == 0 and soil.moisture_value_2 == 1) ):
            msg = "Irrigation required"
            return render_template('succ_pump.html', msg = msg, moisture='Soil moisture level is in between 80% - 90%')
            GPIO.output(21, GPIO.LOW)

        elif ((precp== "WEAK" or precp== "MODERATE" or precp== "ZERO") and (soil.moisture_value_1 == 1 and soil.moisture_value_2 == 1)):
            msg = "Irrigation required"
            return render_template('succ_pump.html', msg = msg, moisture='Soil moisture level is below 80%')
            GPIO.output(21, GPIO.HIGH)
            time.sleep(5)
            GPIO.output(21, GPIO.LOW)

        else:
            msg = "Irrigation not required"
            return render_template('succ.html', msg = msg, moisture='Soil moisture level is above 90%')
            GPIO.output(21, GPIO.LOW)
        
       """
        return render_template('succ_pump.html', msg = msg, moisture='Soil moisture level is above 20%')

@app.route('/pump', methods=['GET', 'POST'])
def pump():
    if request.method == 'POST':
        pump_time = request.form['duration']
        mesg = "Pump started..."
        return render_template('succ_pump2.html', mesg = mesg)
if __name__ == '__main__':
    app.run(debug=True)