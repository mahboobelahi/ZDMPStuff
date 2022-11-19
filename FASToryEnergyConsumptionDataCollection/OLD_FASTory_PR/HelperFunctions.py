import threading,time,requests
from pprint import pprint


import Workstation as WkC


def create_WS_instences(Workstations,LocIP,wLocPort,hav_no_EM ):
    """

    :return: list of Workstation objects
    """
    WS_obj_list = list()


    for i in range(1,len(Workstations)+1):
        if i in hav_no_EM:
            pass
            #temp_obj = WkC.Workstation(Workstations[i - 1], LocIP, wLocPort + i, False)
            #if temp_obj.get_ID() != 1: threading.Thread(target=temp_obj.runApp).start()

            print('\nHF_1_Workstation INFO:')
            #pprint(temp_obj.WkSINFO())
            #WS_obj_list.append(temp_obj)
        else:
            # temp_obj=WkC.Workstation(Workstations[i-1],LocIP,wLocPort+i,True)
            #
            # temp_obj.measurement_service()
            if i==10:
                temp_obj = WkC.Workstation(Workstations[i - 1], LocIP, wLocPort + i, True)
                #temp_obj.measurement_service()
                threading.Thread(target=temp_obj.runApp).start()

                print('\nHF_1_Workstation INFO:')
                pprint(temp_obj.WkSINFO())

                WS_obj_list.append(temp_obj)

    return WS_obj_list


def event_subscriptions(WS_instenceslist_):

        for obj in WS_instenceslist_:
            print('\nSubscription of CNV Zones for Workstation_%d\n' % obj.get_ID())
            for zone_name in range(1, 6):
                if zone_name == 5:
                    continue
                time.sleep(.2)
                obj.CNV_event_subscriptions(zone_name)

            # Robot's Events Subscriptions
            print('\nSubscription of Rob Events for Workstation_%d\n' % obj.get_ID())
            if obj.get_ID() == 1:
                obj.ROB_event_subscriptions('PaperLoaded')
                obj.ROB_event_subscriptions('PaperUnloaded')
            elif obj.get_ID() == 7:
                obj.ROB_event_subscriptions('PalletLoaded')
                obj.ROB_event_subscriptions('PalletUnloaded')
            else:
                obj.ROB_event_subscriptions('PenChangeEnded')
                time.sleep(.2)
                obj.ROB_event_subscriptions('DrawEndExecution')
            #pprint(obj.WkSINFO())

# deleting subscriptions





#invoks EM service
def invoke_measurement_service(WS_instenceslist_):
    """
    This service need one time invokation and coutinously send measurements to
    subscriber untill connection lost or somthing interrupts the Energy Analyzer module.
    Due to this the service is stoped during instentiation of Workstation objects
    :return:
    """
    for obj in WS_instenceslist_:
        if ( obj.get_ID() == 10) and obj.has_EM:
            obj.measurement_service('start')

#Check Zone status


def ZoneStatus():
    load=''
    ZoneStatus=[]
    for i in [1,2,3,5]:
      req= requests.post(f'http://192.168.10.2/rest/services/Z{i}',json={"destUrl" : ""})
      ZoneStatus.append(req.json().get('PalletID'))
    # for j in ZoneStatus:
    #     if j!='-1':
    #         load=load+'1'
    #     if j=='-1':
    #         load = load + '0'
    return ZoneStatus

