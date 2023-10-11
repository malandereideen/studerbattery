import wifimgr
from machine import Pin
from time import sleep
from netzwerk import *
from geheim import *
import display
import time
from ota import OTAUpdater

try:
    import usocket as socket
except:
    import socket
    
timeout = 900

wlan = wifimgr.get_connection()

if wlan is None:
    display.clean()
    display.no_connection()
    while True:
        pass


display.clean()
sleep(1)

firmware_url = "https://github.com/malandereideen/studerbattery/"

ota_updater = OTAUpdater(wifimgr.ssid, wifimgr.password,firmware_url, "main.py")

ota_updater.download_and_install_update_if_available()

while True:
    mytime = wifi.get_zeit()
    mydatum = wifi.date_text(mytime)
    myuhrzeit = wifi.time_text(mytime)
    mybattery = wifi.get_battery(std_uid,std_mail,std_pass)
    display.clean()
    display.zeit(mydatum,myuhrzeit)
    display.scala()
    display.ladung(mybattery)
    sleep(timeout)
        