from configurations import LocIP,LocPort,MQTT_CLIENT_ID,ROBOT_NAME
from pprint import pprint as P
from msgBus import MqqtClient
import socket, time, threading
from FTP_client import download_and_publish_pic
JSON_DATA={"RobotData":[],
            "ImageData":[{"pix/mm":0.623,"format":"PNG",
                        "Width":640,"Height":480,
                        "Part_Z_dimention":-269.974}]
            }

def start_servers():
    global JSON_DATA
    client = MqqtClient(ROBOT_NAME,MQTT_CLIENT_ID)
    client.connect()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((LocIP,LocPort))
    sock.listen(1)
    
    while True:
        print("[X-SC] Waiting for connection...")
        conn, client_address = sock.accept()

        print("[X-SC] Connection from ", client_address)
        
        while True:
            data = conn.recv(1024)
            #print(f'[X-SC] {data}')
            if data != b'':
                data = data.decode().strip().split()
                print(f'[X-SC] {data}')
                if len(data)>1:

                    JSON_DATA["RobotData"].append({
                                        data[0]:dict(
                                        [("XYZ",[float(i) for i in data[1:4] ]),
                                        ("WPR",[float(i) for i in data[4:] ]),
                                        ("CONFIG","NUT000")]
                                        )})
            else:
                print('[X-SC] BREAK LOOP')
                break


        #print('[X-SC] IN LOOP')
        threading.Timer(0.1, download_and_publish_pic,
                args=(JSON_DATA,client)
                ).start()
        #P(JSON_DATA)
        time.sleep(1)
    
    #conn.sendall(data)

            