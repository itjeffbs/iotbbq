### libs and functions ###

import network,select,socket,machine,onewire,ds18x20,time,utime,os,urequests
import uasyncio as asyncio
from network import WLAN
from machine import Pin
from machine import RTC
from umqttsimple import MQTTClient



### MQTT Connection Data ###
mqtt_server = 'broker.mqttdashboard.com'
client_id = 'test_oc'
user_t = 'ocpw_user'
password_t = 'ocpw_pw'
topic_pub = 'PRIMA_COMPOSTING_FINISHED'

def mqtt_connect():
    try:
        client = MQTTClient(client_id,mqtt_server,keepalive=3,port=1883)
        client.connect()
        response = 'Connected to %s MQTT Broker'%(mqtt_server)
    except:
        response = 'Failed to Connected to MQTT Broker'
    print(response)
    return(client)


### Business logic functions ###
def initial_sleep():
    print('Start Sleep')
    time.sleep(7)
    return ('End Sleep')

def connect_to_network():
    try:
        ### Connecto to network ###
        # wifi = 'OC Employee Internet'
        # password = 'Ocit2022!'
        #
        # wifi = 'DMPDR0RSNTHC-iPad'
        # password = '12345678'
        #
        # wifi = 'Verizon-MiFi8800L-8074'
        # password = '89b1b84c'
        #
        wifi = 'OCWR1-2G'
        password = 'prima2021'
        #
        # wifi = 'hammerhead'
        # password = 'sU^J8N54*4'
        
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.config(pm = 0xa11140)  # Disable power-save mode
        wlan.connect(wifi,password)
        max_wait = 3
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                connected = 'WiFi Not Connected'
            max_wait -= 1
            print('waiting for connection...')
            time.sleep(2)

        if wlan.status() != 3:
            connected = 'WiFi Not Connected'
            return(connected)
            raise RuntimeError('network connection failed')
        elif wlan.status() == 3:
            connected = 'WiFi Connected'
    except:
        connected = 'WiFi Not Connected'
    return(connected)


def write_csv():
    try:
        r = open('tempReadings.csv','r')
        for i in r:
            led.on()
            client = mqtt_connect()
            print('client')
            val = str(i)
            client.publish(topic_pub,val)
            time.sleep(2)
            client.disconnect()
        del client
        r.close()
        
        os.remove('tempReadings.csv')
        write_status = 'Connected and written data from csv'
    except:
        write_status = 'csv already pushed, passed'
    return(write_status)



def write_live():
    ### Pinout assignments ###
    sensor_temp = machine.ADC(4)
    sensor_temp_e = Pin(22)
    led = machine.Pin("LED", machine.Pin.OUT)
    ### Sensor variables ###
    sensor_e = ds18x20.DS18X20(onewire.OneWire(sensor_temp_e))
    roms = sensor_e.scan()
    sensor_e.convert_temp()
    try:
        for rom in roms:
            ### get unix time again world time logic
            unixTime = urequests.get("https://worldtimeapi.org/api/timezone/America/Los_Angeles").json().get('unixtime')
            tempval_p = (sensor_e.read_temp(rom)* 9 / 5 + 32)
            stateis_p = str(tempval_p) + ',' + str(unixTime) + str(',1')
            client = mqtt_connect()
            print('client')
            client.publish(topic_pub,stateis_p)
            print(stateis_p + ' loading current reading')
            client.disconnect()
        del client
        connection_status = 'Connected and pushed data'
    except:
        try:
            del client
        except:
            print('no client')
        connection_status ='Failed to connect to wifi or mqtt'
    print (connection_status)

def write_disconnected():
    try:
        for rom in roms:
            rtc=machine.RTC()
            readingTimedate = rtc.datetime()
            readingTime = utime.time() #+ 28800
            tempval_p = (sensor_e.read_temp(rom)* 9 / 5 + 32)
            stateis_p = str(tempval_p) + ',' + str(readingTime) + str(',1')
            print(stateis_p)
            t = open('tempReadings.csv','a')
            t.write(str(stateis_p)+'\n')
            t.close()
            result = 'Succeeded'
    except:
        result = 'Failed'
    print(result)



def parse_datetime():
    try:
        unixTime = urequests.get("https://worldtimeapi.org/api/timezone/America/Los_Angeles").json().get('unixtime')
        dayofWeek = int(urequests.get("https://worldtimeapi.org/api/timezone/America/Los_Angeles").json().get('day_of_week'))
        date_time = urequests.get("https://worldtimeapi.org/api/timezone/America/Los_Angeles").json().get('datetime')
        parsed_datetime = str(date_time).replace('T', ',').replace(':', ',').replace('-', ',')
        parsed = parsed_datetime.split(',')
        y = int(parsed[0])
        month = int(parsed[1])
        d = int(parsed[2])
        h = int(parsed[3])
        minute = int(parsed[4])
        s = parsed[5]
        # (year, month, day, weekday, hours, minutes, seconds, subseconds)
        thedate = (y,month,d,dayofWeek,h,minute,0,255)
        print(thedate)
        rtc = machine.RTC()
        rtc.datetime(thedate)
        print(rtc.datetime())
        time_result = rtc.datetime()
    except:
        time_result = 'Time Not Set'
    return(time_result)




