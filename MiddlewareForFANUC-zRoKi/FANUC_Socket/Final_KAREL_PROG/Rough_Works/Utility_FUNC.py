import time
import requests,threading,json
from requests.auth import HTTPBasicAuth
from client import connect_socket
from FTP_client import download_and_publish_pic

CMD=dict([
            ("open-socket",200),
            ("send-pic",199),
            ("zRokiPOS",198),
            ("close-socket",197)
        ])

# register robot to ZDMP-DAC Component
def register_device(URL,credentials,ID,name):
    # need to set some guard condition to avoid re-registration of device
    # each device registared against a unique external ID
    req= requests.get(url=f'{URL}/deviceInfo?externalId={ID}',
                        auth=HTTPBasicAuth(credentials[0],credentials[1])
                        )
    if req.status_code == 200:
        
        print('[X-UF] Device is already Registered. Device details are:')
        print(f'[X-HU] ID From DAQ: {req.json().get("id")}')
        #pp(req.json())
    else:
        print('[X-UF] Registering the device....')
        req_R= requests.post(url=f'{URL}/registerDevice?externalId={ID}&name={name}&type=c8y_Serial',
                                auth=HTTPBasicAuth(credentials[0],credentials[1])
                                )
        print(f'[X-UF] Http Status Code: {req_R.status_code}')
        # setting souece ID of device
        print(f'[X-HU] ID From DAQ: {req_R.json().get("id")}')
        print('[X-UF] Device Registered Successfully.\n')
        #pp(req_R.json())
        #ID----'38623848'
        """
         I have a question just for my own knowledge, During the test of the TAU middleware application
         I subscribed to a random topic on message bus using the MQTT box (GUI MQTT client) 
         but this client did not receive any published data through the subscribed device was publishing data continuously.
         Can you please provide some insight into this issue? 
        """
#utility Function(S)

#process commands

def process_CMD(cmd,URL_ORC,mqtt):
    if cmd in CMD:
        payload = {"CMD":CMD.get(cmd)}
        if CMD.get(cmd) == 200:
            # run Socket Messing Server 
            r= requests.get(f'{URL_ORC}',params=payload)
            
            print(f'[X-UF] Status Code: {r.status_code}, CMD: {CMD.get(cmd)}')
            print(f'[X-UF] {r.text}')
            threading.Thread(target=connect_socket,args=(mqtt,),
                         daemon = True).start()
            return
        elif CMD.get(cmd) == 199:
            # download current Morkspace picture and publish to zRoki
            r= requests.get(f'{URL_ORC}',params=payload)
            print(f'[X-UF] Status Code: {r.status_code}, CMD: {CMD.get(cmd)}')
            print(f'[X-UF] {r.text}')
            threading.Timer(1, download_and_publish_pic,
                        args=(mqtt,)).start()
            # threading.Thread(target=download_and_publish_pic,args=(mqtt,),
            #              daemon = True).start()
            #return
        elif CMD.get(cmd) == 197:

            r= requests.get(f'{URL_ORC}',params=payload)
    else:
        print("[X-UF] CMD not Understand....")

#update robot position
def update_POS(POS,URL,URL_ORC):
    #[float(val) for val in json.loads(POS).values()]
    id= 100
    (XX,YY,ZZ,WW,PP,RR) = ([float(val) for val in json.loads(POS).values()])
    payload =dict([ ("id",id),
                    ("XX",XX),("YY",YY),("ZZ",ZZ),
                    ("WW",WW),("PP",PP),("RR",RR)
                    ])
    
    r= requests.get(f'{URL}',params=payload)
    print(f'[X-UH] {r.url}')
    time.sleep(0.1)
    r= requests.get(f'{URL_ORC}',params={"CMD":198})
    print(f'[X-UH] {r.url}')
    

    