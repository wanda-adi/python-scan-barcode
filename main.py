#!/usr/bin/env python

import serial
from time import sleep
from rpi_lcd import LCD
import os, json
import requests
from subprocess import call

#url = "http://172.27.6.36:8080/ovis/validasiScaner"
url = "http://local.otics.co.id:8081/ovis/validasiScaner"
files=[]
headers={'Authorization':'Basic b3RpY3NPVklTOm90aWNzT1ZJU0luZG9uZXNpYQ=='}


#setup
lcd = LCD()
item_count=0
counter=0
scan_1=""
scan_2=""
perangkat=""
total_scan=""


'''curl is used to make a http request'''
lcd.text("Scan QRcode ", 1)
cmd="curl -s " + url
print(cmd)
print("\n")


ser_arduino = serial.Serial(
    port='/dev/ttyUSB0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)


ser_lora = serial.Serial(
    port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

try :
    while 1:
        scan_1= str(input())
        lcd.text("Scanned Barcode is", 1)
        lcd.text(scan_1,2)
        lcd.text("   Item Added", 1)
        scan_2= str(input())
        lcd.text("Scanned Barcode is", 1)
        lcd.text(scan_2,2)
        lcd.text("   Item Added", 1)
        item_count=item_count+1
        IC=str(item_count)
        lcd.text("Connecting......",1)
        lcd.text(IC,2)
        total_scan = scan_1 + "," + scan_2
        ser_lora.write(scan_1.encode() + b"," + scan_2.encode())
        lcd.text("", 2)
        item_count = 0

        payload = {
            'scan1':scan_1,
            'scan2':scan_2,
            'perangkat':"Towing-Hikitori-B"
        }
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        
        data_hasil = response.json()
        data2_hasil = data_hasil['messages']
        data3_hasil = data2_hasil['kembalian']
        hasil = data3_hasil['hasil']
        print(hasil)
        
        data_status = response.json()
        data2_status = data_status['messages']
        data3_status = data2_status['kembalian']
        status = data3_status['status']
        print(status)

        if(status =="1"):
            ser_arduino.write(b",oke,23,23,0,")
            print("OKE")
            lcd.text("Data OKE", 1)
        if(status == "0"):
            ser_arduino.write(b",ng,24,24,24,")
            print("NG")
            lcd.text("Data NG", 1)
except:
    print("Gagal")
    lcd.text("Error jaringan!", 1)
    lcd.text("Reset Alat", 2)
    ser_arduino.write(b",sinyal_ng,23,23,0,")
    
    call(["python", "/home/pi/barcode_project/main.py"])
        
