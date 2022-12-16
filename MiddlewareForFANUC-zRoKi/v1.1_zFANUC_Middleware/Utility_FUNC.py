import requests,threading,json,urllib.parse,time
from base64 import b64encode
from datetime import datetime

from configurations import (ROBOT_ID,BASE_TOPIC,
                            ORCHESTRATOR_URL,
                            UPDATE_POS_REG,
                            SYNCH_URL)

# register robot to ZDMP-DAC Component
def register_device(URL,ID,name):
    # need to set some guard condition to avoid re-registration of device
    # each device registared against a unique external ID
    # Cumulocity credentials are not required anymore within ZDMP network
    req= requests.get(url=f'{URL}/deviceInfo?externalId={ID}')
    if req.status_code == 200:
        
        print('[X-UF] Device is already Registered. Device details are:')
        print(f'[X-HU] ID From DAQ: {req.json().get("id")}')
        #pp(req.json())
    else:
        print('[X-UF] Registering the device....')
        req_R= requests.post(url=f'{URL}/registerDevice?externalId={ID}&name={name}&type=c8y_Serial')
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
#send Data to zRoki
def IMG_bytes_to_JSON(image,JSON_DATA):
                # reading newly downloaded file as bytes
                # first: reading the binary stuff
                # note the 'rb' flag
                # result: bytes
                with open(image, 'rb') as file:
                    pub_img = file.read()
                    # second: base64 encode read data
                    # result: bytes (again)
                    base64_bytes = b64encode(pub_img)
                    # third: decode these bytes to text
                    # result: string (in utf-8)
                    base64_string = base64_bytes.decode('utf-8')
                    # with open('img.txt','w') as fl:
                    #     fl.write(base64_string)
                    JSON_DATA.get("ImageData")[0].update({"Picture":base64_string})
                    JSON_DATA.update({"timeStamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S')})
                    return JSON_DATA
       
def parsed_Roki_Msg(Roki_Msg):
    #de-serialize incomming JSON string to python dictionary
    Msg_dict = json.loads(Roki_Msg)
    IK_solutions = Msg_dict.get("InverseKinematicSolutions")
    id =100
    if IK_solutions:
        for j in IK_solutions:
            key,j_angles = list(j.items())[0]
            payload = dict([
                ("id",100),
                ("J1_angel_str",j_angles[0]),
                ("J2_angel_str",j_angles[1]),
                ("J3_angel_str",j_angles[2]),
                ("J4_angel_str",j_angles[3]),
                ("J5_angel_str",j_angles[4]),
                ("J6_angel_str",j_angles[5])])
            print(f'[X-UH] {payload}')
            req= requests.get(f'{UPDATE_POS_REG}',params=payload)
            print(f'[X-UH] {req.text}')
            if int(req.text) == 200:
                print("[X-UH] Reachable POS....")
                time.sleep(0.5)
                req= requests.get(f'{ORCHESTRATOR_URL}',params={"CMD":198})
                print(f'[X-UH] {req.status_code}')
    else:
        print("[X-UH] No IK Solutions....")
        print("[X-UH] Now starting camera cycle...")
        #time.sleep(0.5)
        req= requests.get(f'{ORCHESTRATOR_URL}',params={"CMD":199})
        print(f'[X-UH] {req.status_code}')
 

#update robot position
def update_POS(POS):
    #[float(val) for val in json.loads(POS).values()]
    id= 100
    (XX,YY,ZZ,WW,PP,RR) = ([float(val) for val in json.loads(POS).values()])
    payload =dict([ ("id",id),
                    ("XX",XX),("YY",YY),("ZZ",ZZ),
                    ("WW",WW),("PP",PP),("RR",RR)
                    ])
    
    req= requests.get(f'{UPDATE_POS_REG}',params=payload)
    print(f'[X-UH] {req.url}')
    time.sleep(0.1)
    req= requests.get(f'{ORCHESTRATOR_URL}',params={"CMD":198})
    print(f'[X-UH] {req.url}')

#Robot information cycle 1
def start_camera_cycle():
    req = requests.get(f'{ORCHESTRATOR_URL}', params={"CMD":199})
    print(f'[X-UFF] Status Code: {req.status_code}')    
# ASYNC-Data:

def sub_or_Unsubscribe_DataSource(ASYNCH_URL,ROBOT_ID,subs=False):
    
    if subs:
        req= requests.get(f'{ASYNCH_URL}/unsubscribe',
                params={"externalId":ROBOT_ID,"topicType":'multi' })
        print(f'Subscribing to Data Source: {ROBOT_ID}....')
        req= requests.get(f'{ASYNCH_URL}/subscribe',
                        params={"externalId":ROBOT_ID,"topicType":'multi' })
        if req.status_code ==200:
                print(f'Subscrption Status: {req.status_code} {req.reason}')
        else:
            print(f'Subscrption Status: {req.status_code} {req.reason}')
    else:
        req= requests.get(f'{ASYNCH_URL}/unsubscribe',
                        params={"externalId":ROBOT_ID,"topic":'multi' })

        if req.status_code ==200:
            print(f'Unsubscrption Status: {req.status_code} {req.reason}')
        else:
            print(f'Unsubscrption Status: {req.status_code} {req.reason}')

#SYNCHRONOUSLY sending measurements on custom endpoint
def send_Measurements(JSON_DATA):
    for k, v in JSON_DATA.items():
        # print(k,v)
        # setting query string
        if JSON_DATA.get('[X-TCP14]'):
            print(JSON_DATA.pop('[X-TCP14]'))
        payload = {"externalId": ROBOT_ID,
                   "fragment": f'{BASE_TOPIC}{k}'}
        payload = urllib.parse.urlencode(payload, safe='/')

        req = requests.post(f'{SYNCH_URL}/sendCustomMeasurement',
                            params=payload,
                            json={k: v})
        print('[X-UF]',req.url)
        print('[X-UF]',req.status_code,req.reason)



