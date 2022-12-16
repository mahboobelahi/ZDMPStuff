import threading,subprocess
from flask import Flask
import configurations as CONFIG
import Utility_FUNC
from msgBus import MqqtClient as mqtt


app= Flask(__name__)

#Middleware Routs
#welcom page
@app.route('/')
def welcome():

        return "<h1>welcom from zFANUC-Middleware!</h1>"


if __name__ == '__main__':

    """
        Register robot to ZDMP-DAQ component. It is one time API call and can be
        done using any REST-client like Postman etc. 
    """
    # threading.Timer(0.15, Utility_FUNC.register_device,
    #                 args=(CONFIG.ADMIN_URL,
    #                       CONFIG.ROBOT_ID,
    #                       CONFIG.ROBOT_NAME)
    #                 ).start()

    """
        This API call allows a data source to publish it data to
        ZDMP-Service and Message Bus when ever a measurement from device is recorded 
        on ZDMP-DAQ component. For disabling this feature omit last parameter
    """
    # threading.Timer(0.5, Utility_FUNC.sub_or_Unsubscribe_DataSource,
    #                 args=(CONFIG.ASYNCH_URL, CONFIG.ROBOT_ID, True)
    #                 ).start()
    #threading.Timer(1, subTest.test).start()
    client = mqtt(CONFIG.ROBOT_NAME, CONFIG.MQTT_CLIENT_ID)
    client.connect()
    print(client)
    #Running FLASK app
    app.run(host=CONFIG.LocIP, port=CONFIG.LocPort)