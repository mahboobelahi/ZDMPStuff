#!/usr/bin/env python3
from pprint import pprint as P
import socket,json
from configurations import ( socket_PORT,
                            socket_ServerIP,
                            SYNCH_URL)

"""
    It is local host because roboguide is running on PC
    when you connect to robot through ethernet cable then use the IP 
    of original robot 192.168.1.1
"""
JSON_DATA={}

def connect_socket(client):
    """
    starts socket communication with robot and sends robot's data to DAQ component
    :param SYNCH_URL: ZDMP-DAQ synchronous API
    :return:
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((socket_ServerIP, socket_PORT))

        while True:
            
            data = s.recv(1024)
            if data == b'':
                break
            #print(f'[X-SM] {data}')
            #processing RAW data
            if data and ('[X-TCP]' not in data.decode().strip().split()):
                data = data.decode().strip().split()
                print(f'[X-SM] {data}')
                if len(data)>1:
                    if data[0] not in JSON_DATA:
                        #making python dictionary object
                        JSON_DATA[data[0]] =dict([("XYZ",[float(i) for i in data[1:4] ]),
                                                ("WPR",[float(i) for i in data[4:] ]),
                                                ("CONFIG","NUT000")])
                        #P(list(JSON_DATA.items()))
                        client.publish('LR-Mate/active-frames/Cam_frame',
                                                json.dumps(JSON_DATA.get("camera_frame"))
                                                )
                        # # sending measurements to ZDMP-DAQ using
                        # #custom Fragment endpoint
                        # threading.Timer(0.1, Utility_FUNC.send_Measurements,
                        #                 args=(JSON_DATA,)
                        #                 ).start()
                        