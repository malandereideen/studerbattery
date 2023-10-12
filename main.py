#WIFI
import wifimgr
#OLED Display
from machine import Pin, I2C
import ssd1306
#Sleep and Time
from time import sleep
import time
#OTA Update
from ota import OTAUpdater
#Network
import network
import time
import socket
import ntptime
import requests
import ujson
#API Studer
from geheim import *

#Socket
try:
    import usocket as socket
except:
    import socket
#WLAN Verbindung herstellen
wlan = wifimgr.get_connection()    
#Display initialisieren
i2c = I2C(0, scl=Pin(22), sda=Pin(23))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
#Abfrageinterval
timeout = 30
timezone = 10800
def display_clean():
    oled.fill(0)
    oled.show()

def display_no_connection():
    oled.text("Keine Verbindung",10,10,1)
    oled.text("möglich...",10,25,1)
    oled.text("Bitte Neustart",10,40,1)
    oled.show()
    
def display_update():
    oled.fill(0)
    oled.show()
    oled.text("Update",10,30,1)
    oled.show()
    
def display_wlan():
    oled.text("WLAN",10,10,1)
    oled.text("verbinden...",10,25,1)
    oled.show()

def display_wlan_manage():
    oled.text("StuderBattery",10,10,1)
    oled.text("123456789", 10,25,1)
    oled.text("192.168.4.1",10,40,1)
    oled.text("aufrufen...",10,55,1)
    oled.show()
    
def display_zeit(datum,uhrzeit):
    for i in range(128):
        for j in range(25):
            oled.pixel(i,j,0)
    oled.show()        
    oled.text(datum,25,1,1)
    oled.text(uhrzeit,35,12,1)
    oled.show()
    
def display_scala():
    for i in range(100):
        oled.pixel(i+14,30,1)
        oled.pixel(i+14,44,1)
    for i in range(15):
        oled.pixel(14,30+i,1)
        oled.pixel(114,30+i,1)
    oled.text("0",10,55,1)
    oled.text("50",58,55,1)
    oled.text("100",100,55,1)
    oled.show()
        
def display_ladung(wert):
    for i in range(98):
        for j in range(13):
            oled.pixel(15+i,31+j,0)
    oled.show()
    for i in range(wert):
        for j in range(13):
            oled.pixel(15+i,31+j,1)
    oled.show()

def get_zeit():
        try:
            ntptime.settime()
        except:
            pass
        return time.mktime(time.localtime()) + timezone
    
def date_text(seconds):
        tempzeit = time.localtime(seconds)
        return "{:02d}.{:02d}.{:04d}".format(tempzeit[2],tempzeit[1],tempzeit[0])

def time_text(seconds):
    tempzeit = time.localtime(seconds)
    return "{:02d}:{:02d}:{:02d}".format(tempzeit[3],tempzeit[4],tempzeit[5])

def get_battery():
    Headers = {"PHASH":std_pass,"UHASH":std_mail,}
    response = requests.get("https://api.studer-innotec.com/api/v1/installation/synoptic/" + std_uid,headers=Headers)
    parsed = ujson.loads(response.content)
    battery = parsed["battery"]
    mywert = battery["soc"]
    mywert = int(mywert)
    return mywert
    
    

#Display leeren
display_clean()
sleep(1)
#Firmware auf Updates prüfen
firmware_url = "https://raw.githubusercontent.com/malandereideen/studerbattery/main/"
ota_updater = OTAUpdater(firmware_url,"main.py","boot.py")
ota_updater.download_and_install_update_if_available()



while True:
    mybattery = 0
    mytime = get_zeit()
    mydatum = date_text(mytime)
    myuhrzeit = time_text(mytime)
    while mybattery == 0:
        mybattery = get_battery()
    display_clean()
    display_zeit(mydatum,myuhrzeit)
    display_scala()
    display_ladung(mybattery)
    sleep(timeout)
