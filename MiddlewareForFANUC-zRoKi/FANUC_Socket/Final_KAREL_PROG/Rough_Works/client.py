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
            if data and ('[X]' not in data.decode().split()):
                data = re.sub("\s-",
                    '',
                data.decode()).split()
                print(data)
                if len(data)>1:
                    if data[0] not in JSON_DATA:
                        JSON_DATA[data[0]] =dict([("XYZ",data[1:4]),
                                                ("WPR",data[4:7]),
                                                ("CONFIG",data[7:])])
                        
                        
                    else:
                        JSON_DATA[data[0]]["XYZ"]=data[1:4]
                        JSON_DATA[data[0]]["WPR"]=data[4:7]
                        JSON_DATA[data[0]]["CONFIG"]=data[7:]
                   
                    
                
                # mqtt.publish('LR-Mate/active-frames/Uframe',json.dumps(JSON_DATA.get("uframe_Data")))
                # mqtt.publish('LR-Mate/active-frames/Utool',json.dumps(JSON_DATA.get("utool_Data")))
                # mqtt.publish('LR-Mate/Home-POS',json.dumps(JSON_DATA.get("Home_POS")))
                
                 #json.dumps(dict(key=data.split()))
            
            else:
                print(f'[XX] Last Published Data: \n {JSON_DATA}')
                print(f'[XX] Connection is closed by USER')
                print(f'[XX] Last Published Data:')
                print(f'[XX] {JSON_DATA}')
                break
                
                
