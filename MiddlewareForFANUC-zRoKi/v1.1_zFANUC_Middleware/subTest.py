import json,base64,ssl
import paho.mqtt.client as mqtt
from pprint import pprint
#from  middleware import*



#ZDMP DAQ and M&S BUS
ROBOT_ID = 'E1223hghhjgh50'
ROBOT_NAME = 'LRgfdgdfd-Mate-200iD-4S-'+ROBOT_ID
zMSG_PORT_VPN = 30204
zMSG_TLS_PORT = 8883
z_MSG_URL_VPN = '192.168.100.100'
z_MSG_URL = 'msgbus-zdmp.platform.zdmp.eu'
USER = 'tau'
PASSWORD =  'ZDMP-tau2020!'
TOPIC_TYPE= 'multi'

#Robot-KAREL URLS
ORCHESTRATOR_URL = 'http://192.168.1.1/KAREL/z_Orchstrate'
UPDATE_POS_REG = 'http://192.168.1.1/KAREL/z_getRokiPOS'
#DAQ URLs
ADMIN_URL = f'http://192.168.100.100:30025'
ASYNCH_URL =  f'http://192.168.100.100:30026'
SYNCH_URL = f'http://192.168.100.100:30027' 
count =0
# ZDMP tenant credentials
domain = "https://zdmp-da.eu-latest.cumulocity.com"
# TenantID = "t59849255/mahboob.elahi@tuni.fi"
#define callback

def on_message(client, userdata, message):
    #middleware.handle_mqtt_message(client, userdata, message)
    global count
    count = count+1
    print( message.topic)
    print(type(message.payload.decode("utf-8")))
    payload= json.loads(message.payload)#.decode("utf-8")
    Picture = payload.get("ImageData").get("Picture")
    img = base64.b64decode(Picture)
    print(payload)
    with open(f'img_{count}.png' , "wb") as fh:
        fh.write(img)
    # import base64
    # img_file = message.payload#.get('IMG')

    
    # payload_to_dic=  json.loads(payload) # to dic
    # dict_to_json=  json.dumps(payload_to_dic) # back to json str
    # print(f"Received Message_{count}:")
    # #print(type(message.payload.decode("utf-8")))
    #print(payload)
    # pprint(payload_to_dic)
    # # print(type(dict_to_json))

def on_connect(client, userdata, flags, rc):
    print(rc)
    #client.connect(host=z_MSG_URL,port=8883)#z_MSG_URL, port=zMSG_PORT '116.202.35.210' 18083
    #client.loop_start()


def on_disconnect(client, userdata, rc):
    print("disconnecting reason  "  +str(rc))
    client.connected_flag=False
    client.disconnect_flag=True

#mqtt client
#def test():
client = mqtt.Client(ROBOT_NAME)
client.username_pw_set(USER, PASSWORD)
client.connected_flag=False
client.on_message = on_message
client.on_connect=on_connect
client.on_disconnect = on_disconnect
client.tls_set("ca_certificate.pem",
                        None,
                        None, cert_reqs=ssl.CERT_NONE,
                        tls_version=ssl.PROTOCOL_TLSv1,
                        ciphers=None )#, tls_version=ssl.PROTOCOL_TLSv1_2)
client.tls_insecure_set(True)
client.connect(host=z_MSG_URL,port=8883, keepalive=60)

client.subscribe("LR-Mate/fromFANUC")
#client.subscribe('LR-Mate/receive-trajectory')
client.loop_forever()#.loop_start()
# time.sleep(4)