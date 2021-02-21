from flask import Flask, redirect, url_for, render_template, request
import json
import threading
import time
from spot import play

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    print(request.method)
    if request.method == 'POST':
        time = request.form.get("hour")
        time += ":"
        time += request.form.get("minute")
        
        day0 = request.form.get("day0")
        day1 = request.form.get("day1")
        day2 = request.form.get("day2")
        day3 = request.form.get("day3")
        day4 = request.form.get("day4")
        day5 = request.form.get("day5")
        day6 = request.form.get("day6")

        if(time == ''):
            print("no time set")
        else:
            print(time)
            print(day0)
            
            newalarm = {
                "active": "true",
                "alarms": [{
                    "active": True,
                    "time": time,
                    "days": [
                        day0,
                        day1,
                        day2,
                        day3,
                        day4,
                        day5,
                        day6,
                    ],
                "song": "",
                "artist": "",
                "songURI": ""
                }]
            }
                
        with open('data.json', 'w') as f:
            json.dump(newalarm, f)
        
        return render_template("index.html")

    elif request.method == 'GET':
        print("No Post Back Call")
        return render_template("index.html")
    
    return render_template("index.html")

def checkTime():
    while True:
        today = time.strftime("%a")
        with open('data.json') as f:
            data = json.load(f)
            now = time.strftime("%H:%M")
            for alarm in data['alarms']:
                clock = alarm['time']
                for day in alarm['days']:
                    if(today == day and now == clock):
                        print('ring ring')
                    #else:
                        #print("nix")
        time.sleep(5)

if __name__ == "__main__":
    x = threading.Thread(target=checkTime)
    x.start()
    app.run(debug=True)
