# Anonymous FTP login
from ftplib import FTP
from configurations import FTP_ServerIP,BASE_TOPIC
from Utility_FUNC import IMG_bytes_to_JSON,send_Measurements
import json
"""
    Currently Image data is directly published on ZDMP service and message bus 
"""
IMG_Count=0
def download_and_publish_pic(JSON_DATA,client):#

    global IMG_Count
    IMG_Count =IMG_Count+1
    VIS_LOG_BASE_DIR = 'ud1:/vision/'
    with FTP(FTP_ServerIP) as ftp:
        print(f'[X-FTP] Welcome Msg from Robot: {ftp.getwelcome()}')

        # changing to image log dir
        ftp.cwd(VIS_LOG_BASE_DIR)
        print(f'[X-FTP] Current_Dir: {ftp.pwd()}')

        """
            FANUC FTP server supports minimal commands that's why 
            in pervious version old dir method were used for listing
            all directories.
            With the modification of z_Take_IMG KAREL source file, navigation in
            robot FTP server much simplified.
        """

        #downloading file from FTP-Server

        with open(f'IMG{IMG_Count}.png', 'wb') as local_file:
                    ftp.retrbinary(f'RETR IMG.png', local_file.write)
                    print('[X-FTP] Image downloaded successfully....')
  
            # now: encoding the data to json
            # result: string          
        #send_Measurements(JSON_DATA)
        # with open(f'IMG{IMG_Count}.txt', 'w') as local_file:
        #     ss=IMG_bytes_to_JSON(f'IMG{IMG_Count}.png',JSON_DATA)
        #     x=ss.get("ImageData")[0].get("Picture")
        #     local_file.write(x)
        #     print('[X-FTP] Image downloaded successfully....')
        
        JSON_STR=json.dumps(IMG_bytes_to_JSON(f'IMG{IMG_Count}.png',JSON_DATA),indent=2)
        client.publish_data(f'{BASE_TOPIC}data',JSON_STR)
        print('[X-FTP] Data published successfully....')

                

