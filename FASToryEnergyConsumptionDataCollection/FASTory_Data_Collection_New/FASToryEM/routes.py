import threading
from FASToryEM import UtilityFunctions as helper
from FASToryEM import app,db
from FASToryEM.dbModels import EnergyMeasurements,WorkstationInfo
from flask import render_template,request,jsonify
import requests,json,time
from FASToryEM.configurations import BASE_TOPIC,hav_no_EM
from  flask_mqtt import Mqtt



mqtt = Mqtt(app)
#####MQTT Endpoints################
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc==0:
        pass
        result=WorkstationInfo.query.all()
        print("[X-Routes] connected, OK Returned code=",rc)
        # #subscribe to tpoics
        time.sleep(1)
        mqtt.unsubscribe_all()
        # #mqtt.unsubscribe(BASE_TOPIC)
        # time.sleep(1)
        for  res in result:
            if res.id==10:
                mqtt.subscribe(f'T5_1-Data-Acquisition/DataSource ID: {res.DAQ_ExternalID} - MultiTopic/Measurements/cmd')
                print(f'[X-Routes] Subscribing to Topic: T5_1-Data-Acquisition/DataSource ID: {res.DAQ_ExternalID} - MultiTopic/Measurements/cmd')
                print(f'[X-Routes] {res.id}')    
    else:
        print("[X-Routes] Bad connection Returned code=",rc)

@mqtt.on_subscribe()
def handle_subscribe(client, userdata, mid, granted_qos):
    print('[X-Routes] Subscription id {} granted with qos {}.'
          .format(mid, granted_qos))   

# @mqtt.unsubscribe()
# def handle_unsubscribe(client, userdata, mid):
#     print('Unsubscribed from topic (id: {})'.format(mid))

@mqtt.on_disconnect()
def handle_disconnect():
    mqtt.unsubscribe_all()
    # mqtt.unsubscribe(BASE_TOPIC)
    mqtt.unsubscribe_all()
    print("[X-Routes] CLIENT DISCONNECTED")

#handles commands from MQTT 
##command structure#####
# {
#     "external_ID":"104EM",
#     "E10_Services": "start",
#     "CNV":{"cmd":"start","CNV_section":"both"}
# }
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    try:
        payload=json.loads(message.payload).get('data')
        print(f"[X-Routes] {type(payload)},'??',{payload}")
        #print(f"[X-Routes] {type(payload)},'??',{payload.get('data')}")
        #db will handles
        exID = int(payload.get("external_ID").split('4')[0])
        result = WorkstationInfo.query.get(exID)
        E10_url=result.EM_service_url
        CNV_url = result.CNV_service_url
        url_self = result.WorkCellIP

        if payload.get("E10_Services") !=None and exID not in hav_no_EM:

            cmd = payload.get("E10_Services")
            # res=threading.Thread(target=helper.invoke_EM_service,
            #                             args=(E10_url,cmd),
            #                             daemon=True).start()
            # print('[X-Routes] ',res)
            ######For Simulation#########
            # if cmd == 'stop':
            #     requests.post(url=f'{result.WorkCellIP}/api/stop_simulations',timeout=60)
            # else:
            #     requests.post(url=f'{result.WorkCellIP}/api/start_simulations',timeout=60)
            #############################
        else:
            print(f'[X-Routes] Invalid Command!')

        if payload.get("CNV")!=None:
            if payload.get("CNV").get("cmd") !=None:
                cnv_cmd = payload.get("CNV").get("cmd")
                cnv_section = payload.get("CNV").get("CNV_section").lower()
                if exID in [7,1] and (cnv_section == 'bypass' or cnv_section == 'both'):
                    print(f'[X-Routes] Invalid Command! ')
                else:
                    
                    res= threading.Thread(target=helper.cnv_cmd,
                                                args=((cnv_cmd,cnv_section,CNV_url,url_self)),
                                                daemon=True).start()
                    print('[X-Routes] ',res)
                
    except ValueError:
        print('[X-Routes] Decoding JSON has failed')

########Flask Application Endpoints################


@app.route('/test', methods=['GET','POST'])
def test():
    if  request.method == 'GET':
        requests.post('http://130.230.190.118:2001/em_measurements')
        return render_template('workstations/measurements.html', title='Home')
    else:
        print('Received Some-Thing')
#Welcom Route
@app.route('/', methods = ['GET'])
def home():
    if request.method == 'GET':
        return render_template('orchestrator/home.html', title='Home')

@app.route('/welcome', methods = ['GET'])
def welcome():
    if request.method == 'GET':
        print('[X-Routes]Request Came from: ',request.url)

        return render_template('orchestrator/welcome.html', title='Welcome',url=request.url)
    else:
         print(request.json)

@app.route('/about', methods = ['GET'])
def about():
    if request.method == 'GET':
        print('[X-Routes]Request Came from: ',request.url)

        return render_template('orchestrator/about.html', title='About')

@app.route('/workstations', methods = ['GET'])
def workstation_list():
    if request.method == 'GET':
        print('[X-Routes]Request Came from: ',request.url)
        workstations = WorkstationInfo.query.all()
        return render_template('orchestrator/work_cell.html',title='Worksations',content=workstations)

@app.route('/api/measurements',methods=['GET'])#/<external_id>/<int:num>
def measurements():#external_id,num
    print(request.args.to_dict())
    id = request.args.to_dict().get("external_id").split('4')[0]
    num=int(request.args.to_dict().get("num"))
    power=[]
    voltage = []
    current = []
    measurements = EnergyMeasurements.query.filter_by(WorkCellID=id).order_by(EnergyMeasurements.id.desc())[:int(num)]
    for measure in measurements:
        power.append(measure.Power)
        voltage.append(measure.RmsVoltage)
        current.append(measure.RmsCurrent)
    return jsonify([{"Power":power},{"Voltage":voltage},{"Current":current}])