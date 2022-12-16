import threading, time, requests
from flask import Flask, request
from flask_mqtt import Mqtt
import Utility_FUNC


#########################Middleware CONSTS-Global VARS#########################

#related to middleware app only
app= Flask(__name__)
LocIP = '192.168.1.3'#'192.168.1.2'
LocPort = 3000

#ZDMP DAQ and M&S BUS
ROBOT_ID = 'E122350'
ROBOT_NAME = 'LRMate200iD-4S'
zMSG_PORT = 30204
zMSG_TLS_PORT = 30206
z_MSG_URL = '192.168.100.100'
USER = 'tau'
PASSWORD =  'ZDMP-tau2020!'
Conn_ALIVE = 5

#Robot-KAREL URLS
ORCHESTRATOR_URL = 'http://192.168.1.1/KAREL/z_Orchstrate'
UPDATE_POS_REG = 'http://192.168.1.1/KAREL/z_getRokiPOS'
#DAQ URLs
ADMIN_URL = f'http://192.168.100.100:30025'
ASYNCH_URL =  f'http://192.168.100.100:30026'
SYNCH_URL = f'http://192.168.100.100:30027' 

# ZDMP tenant credentials
domain = "https://zdmp-da.eu-latest.cumulocity.com"
TenantID = "t59849255/mahboob.elahi@tuni.fi"
passward = "mahboobelahi93"
#########################Middleware CONSTS-Global VARS#########################


##############################MQTT-Settings###########################################
app.config['MQTT_CLIENT_ID'] = 'E122350-LRMate200iD-4S'
app.config['MQTT_BROKER_URL'] = z_MSG_URL  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = zMSG_PORT  # default port for non-tls connection
app.config['MQTT_USERNAME'] = USER  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = PASSWORD # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = Conn_ALIVE  # set the time interval for sending a ping to the broker to 5 seconds
#app.config['MQTT_TLS_ENABLED'] = True  # set TLS to disabled for testing purposes
#app.config['MQTT_TLS_CA_CERTS'] = './files/ca_certificate.pem'

mqtt = Mqtt(app)
mqtt.bad_connection_flag=False
mqtt.connected_flag=False
mqtt.disconnected_flag=False
mqtt.suback_flag=False
##############################MQTT-Settings###########################################

#MQTT Section
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):

    if rc==0:
        client.connected_flag=True #set flag
        print("[X-M] connected, OK Returned code=",rc)

        mqtt.subscribe('LR-Mate/CMD')
        mqtt.subscribe('LR-Mate/receive-trajectory')
    else:
        mqtt.bad_connection_flag=True
        print("[X-M] Bad connection Returned code=",rc)


@mqtt.on_disconnect()
def handle_dis_connect(client, userdata, flags, rc):

    print("[X-M] disconnecting reason  "  +str(rc))
    client.connected_flag=False
    client.disconnect_flag=True


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    
    print("[X-M] Received Message")
    data = dict(
        topic=message.topic,
        payload=message.payload.decode("utf-8"),
        QOS=message.qos,
        Retain_FLG=message.retain
    )
    print(f'[X-M] {data}')
    if "CMD" in data.get("topic","Not a valid topic"):
        threading.Thread(target=Utility_FUNC.process_CMD,
        args=(data.get("payload"),
              ORCHESTRATOR_URL,
              mqtt),
        daemon = True).start()
    else:
        threading.Thread(target=Utility_FUNC.update_POS,
        args=(data.get("payload"),
        UPDATE_POS_REG,
        ORCHESTRATOR_URL),
        daemon = True).start()


#Middleware Routs
#welcom page
@app.route('/')
def welcome():

        return ("<h1>welcom</h1>")

if __name__ == '__main__':
        # r=requests.get('http://192.168.1.1/KAREL/z_Orchstrate?CMD=200')
        # print(r.status_code, r.reason)
        threading.Timer(1, Utility_FUNC.register_device,
                        args=(ADMIN_URL,(TenantID, passward),ROBOT_ID,ROBOT_NAME)
                        ).start()
        
        app.run(host=LocIP, port=LocPort,debug=False)



