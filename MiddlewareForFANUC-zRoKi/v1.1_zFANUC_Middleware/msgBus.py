import Utility_FUNC,threading
import paho.mqtt.client as mqtt
from random import randint
import ssl
"""
    Add some random INT to robot ID if your are
    planning to use this class for multiple instence of FANUC robot 
"""
from configurations import (
                            z_MSG_URL_VPN,
                            zMSG_PORT_VPN,
                            MQTT_BROKER_URL,
                            zMSG_TLS_PORT,
                            USER,
                            PASSWORD,
                            Conn_ALIVE,
                            BASE_TOPIC
                            )



class MqqtClient():

    def __init__(self,name,ID):
        self.name = name
        self.ID = ID
        self.client = mqtt.Client(self.ID, clean_session=True,)
        self.client.username_pw_set(USER, PASSWORD)
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscribe = self.on_subscribe


    def connect(self):
        self.client.tls_set("./files/ca_certificate.pem",
                        None,
                        None, cert_reqs=ssl.CERT_NONE,
                        tls_version=ssl.PROTOCOL_TLSv1,
                        ciphers=None )#, tls_version=ssl.PROTOCOL_TLSv1_2)
        self.client.tls_insecure_set(True)#'msgbus-zdmp.platform.zdmp.eu'
        self.client.connect(host='msgbus-zdmp.platform.zdmp.eu', port=zMSG_TLS_PORT,keepalive=Conn_ALIVE)
        self.client.loop_start()

    def publish_data(self,topic,data):
        self.client.publish(topic, data, qos=0, retain=False)

    #define callback

    def on_message(self,client, userdata, message):
        """
        topic base message filtering and processing
        :param client:
        :param userdata:
        :param message: JSON-trajectories or commands
        :return:
        """
        print("[X-Msg] Received Message")
        data = dict(
            topic=message.topic,
            payload=message.payload.decode("utf-8"),
            QOS=message.qos,
            Retain_FLG=message.retain
        )
        #print(f'[X-Msg] {data}')

        threading.Thread(target=Utility_FUNC.parsed_Roki_Msg,
                    args=(data.get("payload"),),
                    daemon=True).start()
        # threading.Thread(target=Utility_FUNC.update_POS,
        #                     args=(data.get("payload"),),
        #                     daemon=True).start()


    def on_connect(self,client, userdata, flags, rc):
        if rc==mqtt.CONNACK_ACCEPTED:
            client.connected_flag=True #set flag
            print("[X-Msg] connected OK Returned code=",rc)
            client.subscribe(f'{BASE_TOPIC}CMD',qos=0)
            client.subscribe(f'{BASE_TOPIC}receive-trajectory',qos=0)
            print(f"[X-Msg] ({BASE_TOPIC}CMD,{BASE_TOPIC}receive-trajectory)")
        else:
            print(f'[X-Msg] Bad connection, Returned code= {rc}')


    def on_disconnect(self,client, userdata, rc):
        print(f'[X-Msg] Disconnecting, returned code: {rc}')
        client.unsubscribe(f'{BASE_TOPIC}CMD')
        print(f"[X-Msg]{self.name}'ve unsubscribed")
        client.unsubscribe(f'{BASE_TOPIC}receive-trajectory')
        print(f"[X-Msg]{self.name}'ve unsubscribed")
        #client.loop_stop()


    def on_subscribe(self,client, userdata, mid, granted_qos):
        print(f"[X-Msg]{self.name}'ve subscribed with QoS: {granted_qos[0]} and mid: {mid}")

    def on_unsubscribe(self,client, userdata, mid, granted_qos):
        print(f"[X-Msg] {self.name}'ve unsubscribed with QoS: {granted_qos[0]}")

