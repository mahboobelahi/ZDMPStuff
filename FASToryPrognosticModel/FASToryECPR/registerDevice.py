# Import libraries
import threading
import time

import requests

from DeviceClass import DeviceClass as makeD_Obj
# #Declare and initialize environment variables:
EMID=[2,3,4,5,6,9,10,11,12]  # S1000 Energy module IDs, named after workstations that have S1000 for monitoring enegy

#C_IoT credentials
TenantID = "t59849255/mahboob.elahi@tuni.fi"
passward = "mahboobelahi93"

def instentiate_DeviceClass_objects():
    EM_devices= list() # contains device objects
    # Local IP and Port for local servers
    LocIP = '192.168.200.200'
    LocPort= 2000
    for EM in EMID:
        temp_obj = makeD_Obj(f'{EM}4EM',EM,LocIP,(LocPort+EM),f'TAU_Workstation_{EM}' )
#        temp_obj.EM_service()
        temp_obj.register_device()
        #starting local server for each device
        threading.Thread(target=temp_obj.runApp).start()
        time.sleep(4)
        requests.get(temp_obj.get_selfURL()+'/playData')

        #threading.Timer(2,temp_obj.EM_service,args=('start',)).start()
        EM_devices.append(temp_obj)

    return  EM_devices

if __name__ == '__main__':
    #instentiating and registering Device Class objects and EM S1000 respectively
    device_Obj= instentiate_DeviceClass_objects()

