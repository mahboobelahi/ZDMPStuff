#!/usr/bin/env python3

import socket,re,json

HOST = '192.168.1.1'  # The server's hostname or IP address
"""
    It is local host because roboguide is running on PC
    when you connect to robot through ethernet cable then use the IP 
    of original robot 192.168.1.1
"""
PORT = 1162      # The port used by the server
JSON_DATA={}


def connect_socket(mqtt):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            data = s.recv(1024)
            if data and ('[X-TCP]' not in data.decode().split()):
                data = re.sub("\s-",
                    '',
                data.decode()).split()

                print(f'[X-M] {data}')
                if len(data)>1:
                    if data[0] not in JSON_DATA:
                        JSON_DATA[data[0]] =dict([("XYZ",[float(i) for i in data[1:4]]),
                                                ("WPR",[float(i) for i in data[4:7]]),
                                                ("CONFIG","NUT000")])

                        
                        # xx=json.dumps(JSON_DATA.get("uframe_Data",'XXUD'))
                        # print(xx)
                    else:
                        JSON_DATA[data[0]]["XYZ"]=[float(i) for i in data[1:4]]
                        JSON_DATA[data[0]]["WPR"]=[float(i) for i in data[4:7]]
                        JSON_DATA[data[0]]["CONFIG"]="NUT000"
                
                        mqtt.publish('LR-Mate/active-frames/Uframe',json.dumps(JSON_DATA.get("uframe_Data",'XXUD')),qos=1)
                        mqtt.publish('LR-Mate/active-frames/Utool',json.dumps(JSON_DATA.get("utool_Data",'XXTD')),qos=1)
                        mqtt.publish('LR-Mate/camera-frame',json.dumps(JSON_DATA.get("camera_frame",'XXCD')),qos=1)
                        mqtt.publish('LR-Mate/Home-POS',json.dumps(JSON_DATA.get("Home_POS",'XXHD')),qos=1)
                        mqtt.publish('LR-Mate/Current-POS',json.dumps(JSON_DATA.get("Current_POS",'XXCD')),qos=1)
                        
                    print(JSON_DATA.items())
            
            else:
                print(f'[XX-SM] Connection is closed by USER')
                print(f'[XX-SM] Last Published Data:')
                print(f'[XX-SM]:\n{JSON_DATA}')
                
                break
                
                
