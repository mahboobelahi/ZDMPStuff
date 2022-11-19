# Import libraries
import json,csv,time,threading

import requests
from requests.auth import HTTPBasicAuth
from flask import Flask, request, jsonify
from pprint import pprint
#environment variables
LocIP = '192.168.200.200'
#DAQ URLs
ADMIN_URL = f'http://192.168.100.100:30025'
ASYNCH_URL =  f'http://192.168.100.100:30026'
SYNCH_URL = f'http://192.168.100.100:30027'

EMID=[2,3,4,5,6,9,10,11,10] # S1000 Energy module IDs, named after workstations that have S1000 for monitoring enegy
# tenant credentials
domain = "https://zdmp-da.eu-latest.cumulocity.com"
TenantID = "t59849255/mahboob.elahi@tuni.fi"
passward = "mahboobelahi93"

class DeviceClass:
    #constructor
    def __init__(self,ex_ID,ID,IP,port,name):
        self.external_ID = ex_ID # device external ID
        self.source_ID = '' # device system ID
        self.LocPort= port
        self.LocIP= IP
        self.name = name
        self.WS_ID= ID
        self.receiveMeasurementsAT= f'http://{IP}:{port}/measurements'
        self.url_self=f'http://{IP}:{port}'
#        self.type = serial # device type

########Class Mutators########
    def get_name(self):
        return self.name

    def get_WS_ID(self):
        return self.WS_ID

    def get_port(self):
        return self.LocPort

    def get_selfURL(self):
        return self.url_self

    def get_device_exID(self):
        return self.external_ID

    def get_source_ID(self):
        return self.source_ID

    # def set_device_exID(self, exID):
    #     self.external_ID = exID

    def set_source_ID(self, srID):
        self.source_ID= srID

########Class Methods########

    def EM_service(self, cmd='stop'):
        body={
            "cmd": cmd,
            "send_measurement_ADDR": self.receiveMeasurementsAT,
            "ReceiverADDR":self.url_self
        }
        URL = f'http://192.168.{self.WS_ID}.4/rest/services/send_all_REST'
        r = requests.post(URL, json=body)
        if cmd == 'stop':
            print(f'\"send_all_REST\" service has been stoped for WS: {self.WS_ID}, {r.status_code}, {r.reason}')
        else:
            print(f'\"send_all_REST\" service has been started for WS: {self.WS_ID}, {r.status_code}, {r.reason}')

    def register_device(self):
        # need to set some guard condition to avoid re-registration of device
        # each device registared against a unique external ID
        req= requests.get(url=f'{ADMIN_URL}/deviceInfo?externalId={self.external_ID}',
                           auth=HTTPBasicAuth(TenantID, passward)
                           )
        if req.status_code == 200:
           self.set_source_ID(req.json().get('id'))
           print('Device already Registered. Device details are:\n')
           #pprint(req.json())
        else:
            print('Registering the device')
            req_R= requests.post(url=f'{ADMIN_URL}/registerDevice?externalId={self.external_ID}&name={self.name}&type=c8y_Serial',
                               auth=HTTPBasicAuth(TenantID, passward)
                               )
            print(f'Http Status Code: {req_R.status_code}')
            # setting souece ID of device
            self.set_source_ID(req_R.json().get('id'))
            print('Device Registered Successfully.\n')
            #pprint(req_R.json())

    def obj_info(self):
        pprint(self.__dict__)

        #while True: time.sleep(100)

    #return f'{req_A}, {req_V} ,{req_P.status_code}'

    # Flask App
    def runApp(self):
        app = Flask(__name__)

        @app.route('/',methods= ['GET','POST'])
        def welcom():
            if request.method == 'POST':
                resp=request.json.get('Msg')
               # print(f'Res from S1000: {resp}')
                resp = json.dumps({'thank': 'yes'}), 200
                return resp
            else:
                return f"<h1>Hello from {self.name}, listening at {self.url_self}<h1>"

        @app.route('/playData', methods= ['GET'])
        def playData():
            id= self.get_device_exID()
            url= self.get_selfURL()
            thread = threading.Timer(.1, publish_measurements,args=(id,url))
            thread.daemon=True
            thread.start()
            return 'OK'

        @app.route('/objectInfo', methods= ['GET'])
        def objt_info():
            return self.__dict__


        #SYNCH part of code
        @app.route('/measurements', methods= ['POST'])
        def measurements():
            #received measurements from S1000
            measurements = request.json
            req_V=requests.post(url=f'{SYNCH_URL}/sendMeasurement?externalId={self.external_ID}&fragment=VoltageMeasurement&value={measurements["rms_voltage_c"]}&unit=V',
                                auth=HTTPBasicAuth(TenantID, passward) )
            req_A=requests.post(url=f'{SYNCH_URL}/sendMeasurement?externalId={self.external_ID}&fragment=CurrentMeasurement&value={measurements["rms_current_c"]}&unit=A',
                                auth=HTTPBasicAuth(TenantID, passward))

            req_P=requests.post(url=f'{SYNCH_URL}/sendMeasurement?externalId={self.external_ID}&fragment=PowerMeasurement&value={measurements["active_power_c"]}&unit=W',
                                auth=HTTPBasicAuth(TenantID, passward) )

            return f'{req_A}, {req_V} ,{req_P.status_code}'

        app.run(host=self.LocIP, port=self.LocPort)

def publish_measurements(external_ID,url):
    with open('s_Measurements10.csv', 'r') as file: #with open('N_Measurements9.csv', 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            time.sleep(1)
            req_V=requests.post(url=f'{SYNCH_URL}/sendMeasurement?externalId={external_ID}&fragment=CurrentMeasurement&value={row["RMS_Current(A)"]}&unit=A',
                                auth=HTTPBasicAuth(TenantID, passward) )
            req_A=requests.post(url=f'{SYNCH_URL}/sendMeasurement?externalId={external_ID}&fragment=VoltageMeasurement&value={row["RMS_Voltage(V)"]}&unit=V',
                                auth=HTTPBasicAuth(TenantID, passward))

            req_P=requests.post(url=f'{SYNCH_URL}/sendMeasurement?externalId={external_ID}&fragment=PowerMeasurement&value={row["Power(W)"]}&unit=W',
                                auth=HTTPBasicAuth(TenantID, passward) )
            print( f'{req_A}, {req_V} ,{req_P.status_code}, {external_ID}')
            # print(row['RMS_Current(A)'],
            #       row['RMS_Voltage(V)'],
            #       row['Power(W)'])
        url=url+'/playData'
        req= requests.get(url)

