#!/usr/bin/env python
import pika
import sys
import ssl
import json
from txtToJson import predict

LOCALHOST = "localhost"
SERVER = "192.168.100.100"
PORT = 30206
USERNAME = "tau"
PASSWORD = "ZDMP-tau2020!"
CA_CERT = "./files/ca_certificate.pem"

EXCHANGE = "amq.topic"
ROUTING_KEY ="T5_1-Data-Acquisition.Datasource ID: 104EM - MultiTopic.Measurements.belt-tension-class-pred"#"output_topic"

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

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(
    exchange=EXCHANGE, queue=queue_name, routing_key=ROUTING_KEY)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    #print(" [x] %r" % (method.routing_key))
    #print(" [x] %r" % (json.loads(body)))
    #predict(**json.loads(body))
    pass


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
