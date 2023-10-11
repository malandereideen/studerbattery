from machine import Pin, I2C
import ssd1306

i2c = I2C(0, scl=Pin(22), sda=Pin(23))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

def clean():
    oled.fill(0)
    oled.show()

def no_connection():
    oled.text("Keine Verbindung",10,10,1)
    oled.text("möglich...",10,25,1)
    oled.text("Bitte Neustart",10,40,1)
    oled.show()
    
def wlan():
    oled.text("WLAN",10,10,1)
    oled.text("verbinden...",10,25,1)
    oled.show()

def wlan_manage():
    oled.text("StuderBattery",10,10,1)
    oled.text("123456789", 10,25,1)
    oled.text("192.168.4.1",10,40,1)
    oled.text("aufrufen...",10,55,1)
    oled.show()
    
def zeit(datum,uhrzeit):
    for i in range(128):
        for j in range(25):
            oled.pixel(i,j,0)
    oled.show()        
    oled.text(datum,25,1,1)
    oled.text(uhrzeit,35,12,1)
    oled.show()
    
def scala():
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
        
def ladung(wert):
    for i in range(98):
        for j in range(13):
            oled.pixel(15+i,31+j,0)
    oled.show()
    for i in range(wert):
        for j in range(13):
            oled.pixel(15+i,31+j,1)
    oled.show()