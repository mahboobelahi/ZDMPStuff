#!/usr/bin/env python3

import socket,time,re,json

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
        #s.sendall(b'100,137.70,79.50,-15.00,-180.00,0.00,90.00')
        # data = s.recv(2024)
        #print(data)
        while True:#data != b'':
            data = s.recv(1024)
            
            # print('[XB] ',data)
            # print('[XD] ',repr(data.decode()))

            #print('Received', repr(data.decode()))
            #print(data.decode().strip().split(' '))
            print('[XX]',('[X]' not in data.decode().split()))
            if data and ('[X]' not in data.decode().split()):
                data = re.sub("\s-",
                    '',
                data.decode()).split()
                #['uframe_Data', '411.096', '215.795', '272.131', '.713', '.059', '89.751', 'N', 'U', 'T,', '0,', '0,', '0']
                #print('[X] ',data)
                if len(data)>1:
                    if data[0] not in JSON_DATA:
                        JSON_DATA[data[0]] =dict([("XYZ",data[1:4]),
                                                ("WPR",data[4:7]),
                                                ("CONFIG",data[7:])])
                        
                        
                    else:
                        JSON_DATA[data[0]]["XYZ"]=data[1:4]
                        JSON_DATA[data[0]]["WPR"]=data[4:7]
                        JSON_DATA[data[0]]["CONFIG"]=data[7:]
                   
                    
                
                mqtt.publish('LR-Mate/Uframe',json.dumps(JSON_DATA.get("uframe_Data")))
                mqtt.publish('LR-Mate/Utool',json.dumps(JSON_DATA.get("utool_Data")))
                mqtt.publish('LR-Mate/Home-POS',json.dumps(JSON_DATA.get("Home_POS")))
                
                 #json.dumps(dict(key=data.split()))
            
            else:
                print(f'[X] {JSON_DATA}')
                break
                
                

# print('Received', type(repr(data.decode())))
# print('Received', data.decode().split(' '))
