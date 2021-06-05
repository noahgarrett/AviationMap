import requests
import json
import time

VFR = "GREEN"
MVFR = "BLUE"
IFR = "RED"
LIFR = "PURPLE"
NO_DATA = "WHITE"

weather_color_map = {"VFR":VFR, "MVFR":MVFR, "IFR":IFR, "LIFR":LIFR}

def getWXMetar(airport):
    hdr = {"X-API-Key": "ce822455b5f84c2788bee768f8"}
    weather = requests.get(f"https://api.checkwx.com/metar/{airport}/decoded", headers=hdr)

    m = weather.json()
    return m["data"][0]["flight_category"]

def getManualWeather(airport):
    hdr = {"X-API-Key": "ce822455b5f84c2788bee768f8"}
    weather = requests.get(f"https://api.checkwx.com/metar/{airport}/decoded", headers=hdr)

    m = weather.json()
    visibility = m['data'][0]['visibility']['miles_float']
    try:
        ceiling = m['data'][0]['ceiling']
        ceiling_feet = ceiling["feet"]
    except:
        ceiling_feet = None

    if ceiling_feet == None:
        return "VFR"

    if visibility > 5 and ceiling_feet > 3000:
        return "VFR"
    elif 3 <= visibility <= 5 or 1000 <= ceiling_feet <= 3000:
        return "MVFR"
    elif 1 <= visibility < 3 or 500 <= ceiling_feet < 1000:
        return "IFR"
    else:
        return "LIFR"




def weatherWXColor():
    airports = ['KALX', 'KAUO', 'KCSG', 'KPXE',
                'KOPN', 'KLGC', 'KLGC', 'KANB',
                'KANB', 'KGAD', 'KCTJ', 'KCCO',
                'KFFC', 'KPUJ', 'KRYY', 'KFTY',
                'KATL', 'KPDK', 'KLZU', 'KD73']

    for i in range(len(airports)):
        weather = getWXMetar(airports[i])
        if weather == "UNK":
            weather = getManualWeather(airports[i])

        try:
            color = weather_color_map[weather]
            print(color)
        except:
            color = NO_DATA

        print(color)

def main():
    while True:
        try:
            weatherWXColor()
            time.sleep(45)
        except Exception as e:
            print(e)
            break

main()
