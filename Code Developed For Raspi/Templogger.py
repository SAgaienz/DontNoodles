from w1thermsensor import W1ThermSensor, SensorNotReadyError, NoSensorFoundError
import sqlite3 as lite
import csv
import time
import numpy
from datetime import datetime
import sys
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT) # HLT
GPIO.setup(24, GPIO.OUT)

# Setup the Database



KENotify = str(input("Press CTL + C to Interrupt Logger. (ENTER to continue)"))
# print(KENotify)
mkTab = str(input('Make Separate Run Table? (name of table if yes, press enter if no) '))

con = None
try:
    con = lite.connect('test.db')

    cur = con.cursor()
    if mkTab == '':
        cur.execute("CREATE TABLE IF NOT EXISTS temperature (name TEXT, volume INT, time DATETIME, tem FLOAT)")
    else:
        cur.execute("CREATE TABLE IF NOT EXISTS "+ mkTab +" (name TEXT, volume INT, time DATETIME, tem FLOAT)")
except:
    print ("Error {}:".format(lite.Error))
    sys.exit(1)

Operation = input("(M)anual of (A)utomatic: ")

nows_date = str(datetime.date(datetime.now()))
Duration_HLT = 0
Duration_BK = 0

HLT_Vol = 0
MT_Vol = 0
BK_Vol = 0
AUX_Vol  = 0


HLT_save = str(input("Save HLT? (y/n) "))
if HLT_save == 'y':
    HLT_Vol = int(input("Volume of HLT (L)? "))
    GPIO.output(23, 1)

MT_save = str(input("Save MT? (y/n)  "))
if MT_save == 'y':
    MT_Vol = int(input("Volume of Mash Tun (L)? "))

BK_save = str(input("Save BK? (y/n)  "))
if BK_save == 'y':
    BK_Vol = int(input("Volume of Boil Kettle (L)? "))
    GPIO.output(24, 1)

AUX_save = str(input("Save Aux? (y/n) "))
if AUX_save =='y':
    AUX_Vol = int(input("Volume of Auxiliry (L)? "))
    
if Operation == "A":
    Duration_HLT = (95-25)*(HLT_Vol*1000*4.2)/3000 *1.2
    Duration_BK = (95-25)*(BK_Vol*1000*4.2)/4000 *1.2
    print("Duration HLT: " + str(Duration_HLT/3600) + 'hrs'  ,"Duration BK: " + str(Duration_BK/3600) + 'hrs')
    print(datetime.now())
elif Operation == "M":
    if HLT_save == 'y' :
        print("Time for HLT")
        Duration_hours = float(input("Hours? "))*3600
        Duration_minutes = float(input("Minutes? "))*60
        Duration_HLT = Duration_hours + Duration_minutes
    if BK_save == 'y':
        print("Time for BK")
        Duration_hours = float(input("Hours? "))*3600
        Duration_minutes = float(input("Minutes? "))*60
        Duration_BK = Duration_hours + Duration_minutes


available_sensors = {
    "0309979453b3": ("HLT", lambda: HLT_Vol),
    "030997944830": ("BK", lambda: BK_Vol),
    "03159779e565": ("MT", lambda: MT_Vol) ,
    "030997944c7e": ("MT", lambda: AUX_Vol)

}

start_time = time.time()
sensor = W1ThermSensor()
while time.time() - start_time < max(Duration_BK, Duration_HLT):
    try:
        for sensor in W1ThermSensor.get_available_sensors():
            
            name, function = available_sensors[sensor.id]

            d = (name, function(), datetime.now().isoformat(), sensor.get_temperature())

            with con:
                cur = con.cursor()
                cur.execute("INSERT INTO temperature VALUES(?,?,?,?)",d)  # 031688e6a2ff 0309979453b3 red

        if time.time() - start_time > Duration_HLT :
            GPIO.output(23, 0)
        if time.time() - start_time > Duration_BK :
            GPIO.output(24, 0)


        DTime_hrs = (max(Duration_BK, Duration_HLT)-time.time()+start_time)/3600
        hours = int(DTime_hrs)
        minutes = (DTime_hrs*60) % 60
        seconds = (DTime_hrs*3600) % 60
        print('Time left of log: '+ "%d:%02d.%02d" % (hours, minutes, seconds), d[0] + ' ' + str(d[3]))
        time.sleep(1)

    except SensorNotReadyError:
        GPIO.output(23, 0)
        GPIO.output(24, 0)
        con.close()
        print("Fuck! When will the sensor ever be ready??!!")
        break
    except KeyboardInterrupt:
        GPIO.output(23, 0)
        GPIO.output(24, 0)    
        con.close()    
        print("KeyboardInterrupt has been caught.")
        break
    except NoSensorFoundError:
        GPIO.output(23, 0)
        GPIO.output(24, 0)    
        con.close()
        print("No Sensors Found.")
        break
GPIO.output(23, 0)
GPIO.output(24, 0)
con.close()
