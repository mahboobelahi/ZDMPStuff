#!/usr/bin/env python
import time

import pika
import sys
import ssl
import json

LOCALHOST = "localhost"
SERVER = "192.168.100.100"
PORT = 30206
USERNAME = "tau"
PASSWORD = "ZDMP-tau2020!"
CA_CERT = "./files/ca_certificate.pem"

EXCHANGE = "amq.topic" 
ROUTING_KEY = "FAST.Belt-Tension.Predict-class"#ititest_injection1_predict_input
def connect_to_bus():
    global channel
    try:
        context = ssl.create_default_context(cafile=CA_CERT)
        ssl_options = pika.SSLOptions(context, LOCALHOST)
        credentials = pika.PlainCredentials(USERNAME, PASSWORD)
        conn_params = pika.ConnectionParameters(host=SERVER,
                            port=PORT,
                            credentials=credentials,
                                                ssl_options=ssl_options)
        connection = pika.BlockingConnection(conn_params)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


    channel = connection.channel()


message=json.dumps({ 
  "json_data": {"ss":123 }
})
def publish_Tclass(data):
    global channel
    # data_out= json.dumps({
    #     "Workstation":data[0],
    #     "ActiveZones": data[1],
    #     "powerConsumption": data[2],
    #     "ABL_T_class":data[3]
    #                       })
    data_out= json.dumps({"data_in":{
        "powerConsumption": data[0],
        "load":data[1]
                          }})
    channel.basic_publish(
        exchange=EXCHANGE, routing_key=ROUTING_KEY, body=data_out)
    print(" [x] Sent %r:%r" % (ROUTING_KEY, str(data_out)))

# while True:
#     channel.basic_publish(
#         exchange=EXCHANGE, routing_key=ROUTING_KEY, body=message)
#     print(" [x] Sent %r:%r" % (ROUTING_KEY, str(message)))
#     time.sleep(1)
# connection.close()
"""
    import emit_to_topic as emit
    emit.connect_to_bus()
    emit.publish_Tclass([0.57,0])
"""