import datetime
from pprint import pprint

import requests
import database as sql
from flask import Flask, request
import HelperFunctions as HF
import numpy as np
# from keras.models import  load_model
# import joblib

energy_meters=[2,3,4,5,6,9,10,11,12]
pallet_objects =dict() # Holds mapped pallet objects from user order
count=0
stop_recording=0
load_comb = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
power =[]
Avg_ratio=[]
Tension_Dict_9= {
    1:0,2:15,3:30,4:45,5:60,6:70,7:75,8:85,9:95
}
Tension_Dict_4= {
    1:[0,15,30,45,60,70],2:75,3:85,4:95
}
Tension_Dict_3= {
    1:[0,15,30,45,60,70],2:[75,85],3:95
}
# # loading Nn model
# model_9 = load_model('M_iter9_2.h5',compile=True)
# CNmodel_3= load_model('NNM_iter3_1.h5',compile=True)
# model_3 = load_model('M_iter3_1.h5',compile=True)
#
# # loading MinMaxScaler Objects
# Load_scaler = joblib.load('pallet-scaler.save')
# Power_scaler = joblib.load('Power-scaler.save')
# Custom_P_scaler = joblib.load('custom-Power-scaler.save')

#workstation class
class Workstation:
    def __init__(self,  ID,wLocIP,wLocPort,flage):
        # workstation attributes

        self.name = f'Workstation_{ID}'
        self.__ID = ID#'SimROB'+str(ID)
        self.__has_EM = flage
        self.Surl = f'http://{wLocIP}:{wLocPort}'
        self.port = wLocPort
        if flage:
            self.measurement_ADD = f'{self.Surl}/measurements'
            self. EM_service_url= f'http://192.168.{ID}.4/rest/services/send_all_REST'
        if ID == 1 or ID == 7:
            self.__hasZone4 = False
        else:
            self.__hasZone4 = True

    # *****************************************
    #  WorkstationClass mutators section
    # *****************************************
    # accessors and setters

    def get_ID(self):
        return self.__ID

    def WkSINFO(self):
        return self.__dict__

    def has_EM(self):
        return self.__has_EM

    def set_has_EM(self,flage):
        self.__has_EM = flage

    # *********************************************
    # auto start/stop energy-measurement service
    # *********************************************
    def measurement_service(self,cmd='stop'):
        body = {
            "cmd": cmd,
            "send_measurement_ADDR": self.measurement_ADD ,
            "ReceiverADDR": self.Surl
        }
        req = requests.post(url=self.EM_service_url, json= body)
        return f'Res: {req.status_code} {req.reason}'

    # *****************************************
    # Record Measurements
    # *****************************************



    def info(self):
        """
        This method gives information of object on which it is called
        :return: object information dictionary
        """
        return self.__dict__

    #*******************************************
    #   Flask Application
    #*******************************************

    def runApp(self):
        """
        Set the flask application
        :return:none
        """
        app = Flask(__name__)
        app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
        #welcom route
        @app.route('/', methods=['GET','POST'])
        def welcom():
            if request.method == 'GET':
                return '<h2>Hello from  Workstation_' + str(self.__ID) + '! Workstation_request.url :=  ' + request.url+'<h2>'
            else:
                    if request.json.get("Msg"):
                        print(f'{self.get_ID()} {request.json.get("Msg")}')
                    elif request.json.get("Msg-id") == "Error":
                        print('Command Status at Workstation {ID} is: Command \' {command} \': is not recognized.'
                              .format( ID=request.json.get('CellID'), command=request.json.get("cmd_status")
                                       ))
                        print('Available Commands are:\n 1.{main}\t\t2.{bypass}\t3.{both}'.format(main='main',bypass='bypass',both='both'))
                    else:
                            print('CNVs Status at Workstation {ID} are: Main: {main}  , Bypass:{bypass}'
                                  .format( ID=request.json.get('CellID'), main=request.json.get("mt_main Status"),
                                           bypass=request.json.get("mt_by Status")
                                           ))
            return ''

        @app.route('/predict', methods=["POST"])
        def predict():
            pass

        # energy measurements will receive here
        @app.route('/measurements', methods= ['GET','POST'])
        def received_measurements():
            global count, power, stop_recording
            load=0
            comb='0000'
            Class=1
            label=0
            # Zone status
            active_zones= HF.ZoneStatus()
            print(active_zones)
            if active_zones[0] != '-1':
                load= 1
                comb= '1000'
                Class=1
                label=1
            if(active_zones[1] != '-1'):
                load= 2
                comb= '0100'
            if(active_zones[2] != '-1'):
                load= 4
                comb= '0010'
            if(active_zones[3] != '-1'):
                load= 8
                comb= '0001'
            if(active_zones[0] != '-1' and active_zones[1] != '-1'):
                load= 3
                comb= '1100'
                Class=2
                label=2
            if(active_zones[0] != '-1' and active_zones[2] != '-1'):
                load= 5
                comb= '1010'
            if(active_zones[1] != '-1' and active_zones[2] != '-1'):
                load= 6
                comb= '0110'
            if(active_zones[0] != '-1' and active_zones[3] != '-1'):
                load= 9
                comb= '1001'
            if(active_zones[1] != '-1' and active_zones[3] != '-1'):
                load=10
                comb= '0101'
            if(active_zones[2] != '-1' and active_zones[3] != '-1'):
                load= 12
                comb= '0011'
            if(active_zones[0] != '-1' and active_zones[1] != '-1' and active_zones[2] != '-1'):
                load= 7
                comb= '1110'
                Class=2
                label=3
            if(active_zones[0] != '-1' and active_zones[1] != '-1' and active_zones[3] != '-1'):
                load= 11
                comb= '1101'
            if(active_zones[0] != '-1' and active_zones[2] != '-1' and active_zones[3] != '-1'):
                load= 13
                comb= '1011'
            if(active_zones[1] != '-1' and active_zones[2] != '-1' and active_zones[3] != '-1'):
                load= 14
                comb= '0111'
            if(active_zones[0] != '-1' and active_zones[1] != '-1' and active_zones[2] != '-1' and active_zones[3] != '-1'):
                load= 15
                comb= '1111'
                Class=2
                label=4
            # else:
            #     load=0
            #     comb= '0000'
            ################################
            power.append(request.json.get("active_power_c"))
            count =count+1
            #Averaging the power
            if count ==10 and stop_recording<=500:
                Avg_P = round(sum(power)/len(power),3)
                #################################################
                #Predict section
                # features_1= np.array(np.append( Power_scaler.transform( [[Avg_P]] ), Load_scaler.transform( [[load]] ) ), ndmin=2)
                # features_2= np.array(np.append( Custom_P_scaler.transform( [[Avg_P]] ), Load_scaler.transform( [[load]] ) ), ndmin=2)
                # pred =model_3.predict(features_1)
                # pred = np.argmax(pred, axis = 1)
                # pred_CN = CNmodel_3.predict(features_2)
                # pred_CN= np.argmax(pred_CN, axis = 1)
                # print(f'Load_{load}, Comb_{comb}, Active_Zone_{active_zones}, Power_{Avg_P}')
                # sql.insert_Pred_data(('Model_3',3,Avg_P,load,comb,int(pred[0]),int(pred_CN[0]),
                #                                 datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
                #
                # sql.insert_Pred_data(('CN_Model_3',3,Avg_P,load,comb,int(pred[0]),int(pred_CN[0]),
                #                                 datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
               #################################################
            #       Data Collection
            #     ratio = round((Avg_P / 1000) * 100,3)
            #     measurements_4_phase_C = (
            #         request.json.get('rms_current_c'),  #"RMS Current (A)":
            #         request.json.get("rms_voltage_c"),  #"RMS Voltage (V)":
            #         request.json.get("power_factor_c"),  #"PF"
            #         # request.json.get("scaled_active_energy_c"),  # "Active_Energy(KW-Hr)":
            #         # request.json.get("active_energy_c"),  #"Active_Energy(W-Hr)":
            #         request.json.get("scaled_active_power_c"),  #"Power(KW)":
            #         Avg_P,  # "Power(W)":
            #         ratio,  # "%Power/Nominal_Power":
            #         label,  # "Label":
            #         Class,  #"Class":,
            #         datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            #              )
            #     sql.insert_EM_data(measurements_4_phase_C)
            #     print(f'Power: {power}, AvgPower: {Avg_P}?????Stop Status:_{stop_recording}')
            #     pprint(measurements_4_phase_C)
            #     count = 0
            #     stop_recording = stop_recording+1
            #     power.clear()
            # print(f'Power_out: {request.json.get("active_power_c")}')


            return 'OK'

        app.run(host= '0.0.0.0',port=self.port,threaded = True)
