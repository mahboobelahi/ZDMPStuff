import requests, csv, time
import configurations as CONFIG
from keras.models import  load_model
import joblib
import numpy as np

import emit_to_topic as emit
#emit.connect_to_bus()



model_3 = load_model('M_iter3_1.h5',compile=True)

# loading MinMaxScaler Objects
Load_scaler = joblib.load('pallet-scaler.save')
Power_scaler = joblib.load('Power-scaler.save')

def sub_or_Unsubscribe_DataSource(ASYNCH_URL,DEVICE_ID,subs=False):
    
    if subs:
        req= requests.get(f'{ASYNCH_URL}/unsubscribe',
                params={"externalId":DEVICE_ID,"topicType":'multi' })
        print(f'Subscribing to Data Source: {DEVICE_ID}....')
        req= requests.get(f'{ASYNCH_URL}/subscribe',
                        params={"externalId":DEVICE_ID,"topicType":'multi' })
        if req.status_code ==200:
                print(f'Subscrption Status: {req.status_code} {req.reason}')
        else:
            print(f'Subscrption Status: {req.status_code} {req.reason}')
    else:
        req= requests.get(f'{ASYNCH_URL}/unsubscribe',
                        params={"externalId":DEVICE_ID,"topic":'multi' })

        if req.status_code ==200:
            print(f'Unsubscrption Status: {req.status_code} {req.reason}')
        else:
            print(f'Unsubscrption Status: {req.status_code} {req.reason}')

def publish_measurements(external_ID,url):
    with open(CONFIG.FILE_NAME, 'r') as file: #with open('N_Measurements9.csv', 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            
            Power = row["Power (W)"]
            load = row["Load Combinations"]
            features_1= np.round(np.array(np.append( Power_scaler.transform( [[Power]] ),
                                 Load_scaler.transform( [[load]] ) ),
                                  ndmin=2),4)
            #emit.publish_Tclass([features_1[0][0],features_1[0][1]])
            #pred = model_3.predict(features_1)
            #pred = np.argmax(pred, axis = 1)[0]
            #print(f'Load_{load}, Power_{Power}, {features_1}')
            #print(pred) 
            payload = {"externalId":external_ID,
                       "fragment": f'belt-tension-class-pred'
                        }   
            try:
                req_pred = requests.post(f'{CONFIG.SYNCH_URL}/sendCustomMeasurement',
                                            params=payload,
                                            json={"powerConsumption": features_1[0][0],
                                                    "load":features_1[0][1]})#json={"class_pred": str(pred)
                req_V=requests.post(url=f'{CONFIG.SYNCH_URL}/sendMeasurement?externalId={external_ID}&fragment=CurrentMeasurement&value={row["RMS Current (A)"]}&unit=A')
                req_A=requests.post(url=f'{CONFIG.SYNCH_URL}/sendMeasurement?externalId={external_ID}&fragment=VoltageMeasurement&value={row["RMS Voltage (V)"]}&unit=V')
                req_P=requests.post(url=f'{CONFIG.SYNCH_URL}/sendMeasurement?externalId={external_ID}&fragment=PowerMeasurement&value={row["Power (W)"]}&unit=W' )

                print( f'{req_A.status_code}, {req_V.status_code}, {req_P.status_code}, {req_pred.status_code}, {external_ID}',{row["Class_3"]})
                
            except requests.exceptions.RequestException as e:
                print("[X] ",e)
            
            time.sleep(5)
            # print("[X] RMS_Current(A)",row.get('RMS Current (A)','Key-Not-Found'),
            #       "RMS_Voltage(V)",row.get('RMS Voltage (V)','Key-Not-Found'),
            #       "Power(W)",row.get('Power(W)','Key-Not-Found'))

        url=url+'/simulate'
        req= requests.get(url)
        print(req.status_code, 'All records have been processed.')

