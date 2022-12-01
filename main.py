### date calc in velocity if needed ###
# umqtt simple download
# https://raw.githubusercontent.com/RuiSantosdotme/ESP-MicroPython/master/code/MQTT/umqttsimple.py

import libs
from libs import *

def main():     
    writewait = 0
    while True:

        ### Start off with sleep, break script during this time when testing ###
        print(libs.initial_sleep())
        conn = libs.connect_to_network()

        if conn == 'WiFi Connected':
            try:
                ### Connect to Network ###
                conn = libs.connect_to_network()
                print(conn)

                ### Set Datetime on connection ###
                libs.parse_datetime()

                ### Write Data While Connected from CSV ###
                print(libs.write_csv())
                
                ### Write Live Data While Connected ###
                print(libs.write_live())
                
                writewait = 0
                connected_push = 'Connected Data Push Succeeded'
            except:
                connected_push = 'Connected Data Push Failed'
            print(connected_push)
   
        else:
            writewait += 1
            if writewait > 2:
                libs.write_disconnected()
                writewait = 0
                disconnected_push = 'Disconnected Data Push Succeeded'
            else:
                disconnected_push = 'Disconnected Data Push Failed'
            print(disconnected_push)
            print(writewait)


if __name__ == '__main__':
    main()
