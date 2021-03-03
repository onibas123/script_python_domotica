#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################
######## RASPBERRY PI 3 MODEL B CONTROLLER       #
##############################################

##############################################
######## IMPORTS                                 #
##############################################
#linux OS
from Tkinter import *
#windows OS
#from tkinter import *
import requests
import RPi.GPIO as GPIO
import time
import re

##############################################
######## CONS                                    #
##############################################

#[server_ws]
URL = "http://192.168.1.100/access_control/index.php/CWSAccess_Control/getAccessPeopleReader"
#[pins]
PIN_SUCCESS = ""
PIN_FAIL = ""
PIN_AUX1 = ""
PIN_AUX2 = ""
PIN_AUX3 = ""
#[time]
SECONDS_SUCCESS = 5
SECONDS_FAIL = 3
SECONDS_AUX1 = 0.1
SECONDS_AUX2 = ""
SECONDS_AUX3 = ""
#[sensor]
SENSOR_ID = 1
ACTION = 0
#[door]
DOOR_ID = 1
LEVEL = 0
#[display]
UBICATION = "PORTERIA PRINCIPAL"
TITLE = "CAPTURADOR DE RUT ENTRADA"
COUNT = 0
##############################################
######## FUNCTIONS                               #
##############################################

def button_callback(channel):
        global ACTION
        if (ACTION == 0):
                #PASA DE INGRESO A SALIDA
                ACTION = 1
                #ACTIVAR GPIO 20
                pin = 20
                GPIO.output(pin, True)
                pin = 21
                GPIO.output(pin, False)
        else:
                #PASA DE SALIDA A INGRESO
                ACTION = 0
                #ACTIVAR GPIO 21
                GPIO.setwarnings(False)
                pin = 21
                GPIO.output(pin, True)
                pin = 20
                GPIO.output(pin, False)

def getAccess(event):
        rutClean = rut.get()
        if "RUN" in rutClean:
                rutClean = re.search("RUN=(.+?)&type", rutClean).group(1).replace("-","")
        else:
                if rutClean[:8].isdigit():
                        rutClean = rutClean[:9]
                else:
                        rutClean = ""
        ####################################################################################
        if len(rutClean)  >= 8 and len(rutClean) <= 9:
                API_ENDPOINT = URL
                data = {'rut': rutClean, 'action': ACTION, 'sensors_id': SENSOR_ID, 'doors_id': DOOR_ID, 'level': LEVEL, 'ubication': UBICATION}
                try:
                        r = requests.post(url = API_ENDPOINT, data = data, timeout=1)
                        response = r.text
                        rut.set("")
                except requests.exceptions.RequestException as e: # This is the correct syntax
                        rut.set("")
        else:
                rut.set("")

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use GPIO number

GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(14,GPIO.RISING,callback=button_callback, bouncetime=400) # Setup event on GPIO 15 rising edge


#PASA DE SALIDA A INGRESO
#ACTIVAR GPIO 20
pin = 20
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, True)
#DESACTIVAR GPIO 21
pin = 21
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, False)


ventana = Tk()
#ventana = tk()
ventana.winfo_screenheight()
ventana.winfo_screenwidth()
# no permite el rezizable de las pantallas
ventana.resizable(0,0)

# ancho x alto
ventana.geometry('500x200')
ventana.configure(bg = 'beige')
#titulo ventana
ventana.title(TITLE)


# genera evento enter
ventana.bind('<Return>', getAccess)
ventana.bind("<Tab>", lambda e: "break")
# definir variable rut
rut = StringVar()


#vincular variable con caja de texto y posicionamiento de esta...
input_rut = Entry(ventana, textvariable=rut)
input_rut.place(x=180, y=100)
input_rut.focus()
#ttk.Button(ventana, text='Mostrar', command=nombre_evento).pack(side=BOTTOM)

ventana.mainloop()



#################################################################################
#################################################################################
