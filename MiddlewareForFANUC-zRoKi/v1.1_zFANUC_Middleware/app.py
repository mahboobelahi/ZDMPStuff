import threading,Utility_FUNC
from flask import Flask,request
import configurations as CONFIG
from SocketServer_zv1_0 import start_servers
app= Flask('__name__')

##############################MQTT-Settings###########################################

#Middleware Routs
#welcom page
@app.route('/')
def welcome():
        
        return ("<h1>welcom from zFANUC Middleware App!</h1>")


if __name__ == '__main__':
    """
        Register robot to ZDMP-DAQ component. It is one time API call and can be
        done using any REST-client like Postman etc. 
    """
    # threading.Timer(1, Utility_FUNC.register_device,
    #                 args=(CONFIG.ADMIN_URL,CONFIG.ROBOT_ID,CONFIG.ROBOT_NAME)
    #                 ).start()

    """
        This API call allows a data source to publish it data to
        ZDMP-Service and Message Bus when ever a measurement from device is recorded 
        on ZDMP-DAQ component. For disabling this feature omit last parameter
    """
    # threading.Timer(0.5, Utility_FUNC.sub_or_Unsubscribe_DataSource,
    #                 args=(CONFIG.ASYNCH_URL, CONFIG.ROBOT_ID, True)
    #                 ).start()

    
    #MQTT and Socket servers will run in child thread
    clients=threading.Timer(2,start_servers)
    clients.daemon=True
    clients.start()
    #start camera cycle 
    cam_cycle=threading.Timer(3, Utility_FUNC.start_camera_cycle)
    cam_cycle.daemon=True
    cam_cycle.start()
    #Run FLASK app
    app.run(host=CONFIG.LocIP, port=CONFIG.FlaskPort)