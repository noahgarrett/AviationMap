import time
from rpi_ws281x import *
import argparse
import requests

# LED strip configuration:
LED_COUNT      = 20      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


# Weather Variables
BASE_URL = "https://api.aviationapi.com/v1"
METAR_URL = "/weather/metar?apt="
VFR = Color(0,255,0)
MVFR = Color(0,0,255)
IFR = Color(255,0,0)
LIFR = Color(255,0,255)
NO_DATA = Color(255,255,255)
BLANK_COLOR = Color(0,0,0)

weather_color_map = {"VFR":VFR, "MVFR":MVFR, "IFR":IFR, "LIFR":LIFR}

# Map Functions
def getMetar(airport):
    weather = requests.get(f'{BASE_URL}{METAR_URL}{airport}')
    m = weather.json()
    return m[airport]['category']
        
def weatherColor(strip):
    # airports[6] = 7A5
    airports = ['KALX', 'KAUO', 'KCSG', 'KPXE',
                'KOPN', 'KLGC', 'KLGC', 'KANB',
                'KANB', 'KGAD', 'KCTJ', 'KCCO',
                'KFFC', 'KPUJ', 'KRYY', 'KFTY',
                'KATL', 'KPDK', 'KLZU', 'KD73' ]
    
    for i in range(len(airports)):
        weather = getMetar(airports[i])
        print(i)
        print(airports[i])
        try:
            color = weather_color_map[weather]
        except:
            color = NO_DATA
        
        
        strip.setPixelColor(i, color)
        strip.show()
        
# Setup Function            
def testColors():
    colorList = [Color(255,0,0), Color(0,255, 0), Color(0,0,255)]
    for i in range(len(colorList)):
        for j in range(0,5):
            strip.setPixelColor(j, colorList[i])
            strip.show()
            time.sleep(1)

def boardWipe(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(0.4)

# Main program logic follows:
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    while True:
        try:
            weatherColor(strip)
            time.sleep(350)
            
        except Exception as e:
            boardWipe(strip)
            print(f'An error has occured, please contact Jerboa Technologies, LLC\nError: {e}')
