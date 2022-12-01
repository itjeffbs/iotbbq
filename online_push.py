import libs
from libs import *

def main():
    while True:
        ### initial sleep interval ###
        print(libs.initial_sleep())

        ### Pinout assignments ###
        sensor_temp = machine.ADC(4)
        sensor_temp_e = Pin(22)
        led = machine.Pin("LED", machine.Pin.OUT)
        ### Sensor variables ###
        sensor_e = ds18x20.DS18X20(onewire.OneWire(sensor_temp_e))
        roms = sensor_e.scan()
        sensor_e.convert_temp()

        conn = libs.connect_to_network()
        print(conn)

        ### Write Live Data While Connected ###
        try:
            for rom in roms:
                ### get unix time again world time logic
                unixTime = urequests.get("https://worldtimeapi.org/api/timezone/America/Los_Angeles").json().get('unixtime')
                tempval_p = (sensor_e.read_temp(rom)* 9 / 5 + 32)
                stateis_p = str(tempval_p) + ',' + str(unixTime) + str(',1')
                client = libs.mqtt_connect()
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


if __name__ == '__main__':
    main()

