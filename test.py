import requests
import json
import time

VFR = "GREEN"
MVFR = "BLUE"
IFR = "RED"
LIFR = "PURPLE"
NO_DATA = "WHITE"

BASE_URL = "https://api.aviationapi.com/v1"
METAR_URL = "/weather/metar?apt="

weather_color_map = {"VFR":VFR, "MVFR":MVFR, "IFR":IFR, "LIFR":LIFR}

def getWXMetar(airport):
    weather = requests.get(f'{BASE_URL}{METAR_URL}{airport}')
    m = weather.json()
    return m[airport]['category']

def getManualWeather(airport):
    weather = requests.get(f'{BASE_URL}{METAR_URL}{airport}')
    m = weather.json()

    visibility = m[airport]['visibility']
    try:
        ceiling_feet = float(m['sky_conditions'][0]['base_agl'])
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
        if weather == "":
            weather = getManualWeather(airports[i])

        try:
            color = weather_color_map[weather]
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

# hdr = {"X-API-Key": "ce822455b5f84c2788bee768f8"}
# weather = requests.get(f"https://api.checkwx.com/metar/KPUJ/decoded", headers=hdr)
# m = weather.json()
# visibility = m['data'][0]['visibility']
#
# print(m['data'][0]['ceiling'])


