import threading, time, requests
from flask import Flask, request
from flask_mqtt import Mqtt
import configurations as CONFIG
import Utility_FUNC
app= Flask('__name__')

##############################MQTT-Settings###########################################

app.config['MQTT_CLIENT_ID'] = CONFIG.MQTT_CLIENT_ID
app.config['MQTT_BROKER_URL'] = CONFIG.z_MSG_URL  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = CONFIG.zMSG_PORT  # default port for non-tls connection
app.config['MQTT_USERNAME'] = CONFIG.USER  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = CONFIG.PASSWORD # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = CONFIG.Conn_ALIVE  # set the time interval for sending a ping to the broker to 5 seconds
#app.config['MQTT_TLS_ENABLED'] = CONFIG.MQTT_TLS_ENABLED  # set TLS to disabled for testing purposes
#app.config['MQTT_TLS_CA_CERTS'] = CONFIG.MQTT_TLS_CA_CERTS
#app.config['MQTT_REFRESH_TIME'] = CONFIG.MQTT_REFRESH_TIME  # refresh time in seconds

mqtt = Mqtt(app)


#MQTT Section
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    """
    On-connect subscriptions to topics
    :param client: MQTT client-obj
    :param userdata: N/A
    :param flags:
    :param rc: status code
    :return: N/A
    """
    #is connection SUCCESS?
    if rc==0:
        print("[X-M] connected, OK Returned code=",rc)
        #subscribe to tpoics
        mqtt.subscribe('LR-Mate/CMD')
        mqtt.subscribe('LR-Mate/receive-trajectory')
    else:
        print("[X-M] Bad connection Returned code=",rc)

# Does not accept any parameter, WHY???????
@mqtt.on_disconnect()
def handle_disconnect():#client, userdata, flags, rc
    """
    handles dic-connections
    :return:
    """
    print("[X-M] disconnecting reason")


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    """
    topic base message filtering and processing
    :param client:
    :param userdata:
    :param message: JSON-trajectories or commands
    :return:
    """
    print("[X-M] Received Message")
    data = dict(
        topic=message.topic,
        payload=message.payload.decode("utf-8"),
        QOS=message.qos,
        Retain_FLG=message.retain
    )
    print(f'[X-M] {data}')
    if "CMD" in data.get("topic", "Not a valid topic"):
        threading.Thread(target=Utility_FUNC.process_CMD,
                         args=(data.get("payload"),
                               CONFIG.ORCHESTRATOR_URL,
                               mqtt, CONFIG.SYNCH_URL),
                         daemon=True).start()
    else:
        threading.Thread(target=Utility_FUNC.update_POS,
                         args=(data.get("payload"),
                               CONFIG.UPDATE_POS_REG,
                               CONFIG.ORCHESTRATOR_URL),
                         daemon=True).start()

#Middleware Routs
#welcom page
@app.route('/')
def welcome():

        return ("<h1>welcom</h1>")


if __name__ == '__main__':
    """
        Register robot to ZDMP-DAQ component. It is one time API call and can be
        done using any REST-client like Postman etc. 
    """
    # threading.Timer(1, Utility_FUNC.register_device,
    #                 args=(ADMIN_URL,ROBOT_ID,ROBOT_NAME)
    #                 ).start()

    """
        This API call allows a data source to publish it data to
        ZDMP-Service and Message Bus when ever a measurement from device is recorded 
        on ZDMP-DAQ component. For disabling this feature omit last parameter
    """
    threading.Timer(1, Utility_FUNC.sub_or_Unsubscribe_DataSource,
                    args=(CONFIG.ASYNCH_URL, CONFIG.ROBOT_ID, True)
                    ).start()

    #Running FLASK app
    app.run(host=CONFIG.LocIP, port=CONFIG.LocPort)