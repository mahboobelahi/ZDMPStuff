
import threading, database, datetime
import time

from flask import Flask, request, redirect
import HelperFunctions as HF
app = Flask(__name__)

#globals for application
LocIP = '0.0.0.0'#'192.168.100.100'
LocPort = 1064
WorkStations = [1,2,3,4,5,6,7,8,9,10,11,12]
wLocIP = '192.168.100.100'
wLocPort = 2000
hav_no_EM = [1,7,8]


#Welcom Route
@app.route('/', methods = ['GET', 'POST'])
def welcom():
    if request.method == 'GET':
        print('Request Came from: ',request.url)
        return '<h2>Hello from  Orchestrator_ ! Workstation_request.url :=  ' + request.url+'<h2>'
    else:
         print(request.json)

if __name__ == '__main__':
    # DB table creation
    #database.create_data_table('EM_Data')
    #database.prediction_Data_table('Prediction_Data')
    #database.alert_Column()
    # Workstation Objects
    WS_instenceslist_ = HF.create_WS_instences(WorkStations,wLocIP,wLocPort,hav_no_EM )
    #invoke measurement service on energy analyzer module
    #threading.Timer(5,HF.invoke_measurement_service,args=(WS_instenceslist_,)).start()
    app.run(host=LocIP, port=LocPort,threaded = True)

