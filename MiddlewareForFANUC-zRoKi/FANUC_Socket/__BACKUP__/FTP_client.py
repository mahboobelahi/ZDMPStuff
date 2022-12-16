# Anonymous FTP login
from ftplib import FTP
HOST = '192.168.1.1'

def download_and_publish_pic(mqtt):
    #uncomment following lines during deployment
    VIS_LOG_BASE_DIR = 'ud1:/vision/logs/'#y21oct21/sub00000
    

    with FTP(HOST) as ftp:
        print(f'[X-FTP] Welcom Msg from Robot: {ftp.getwelcome()}')
        # working with directories
        
        print(f'[X-FTP] Root_Dir: {ftp.pwd()}')  # Usually default is md:\ memory device
        ftp.cwd(VIS_LOG_BASE_DIR) #fr:/vision/data
        print(f'[X-FTP] Current_Dir: {ftp.pwd()}')
        
        #List files
        files = []
        ftp.dir(files.append)  # Takes a callback for each file
        VIS_LOG_BASE_DIR=VIS_LOG_BASE_DIR+max(files[-1].split(' '))+'/'
        ftp.cwd(VIS_LOG_BASE_DIR)
        files.clear()
        ftp.dir(files.append)
        VIS_LOG_BASE_DIR=VIS_LOG_BASE_DIR+max(files[-1].split(' '))

        # VIS_LOG_BASE_DIR=VIS_LOG_BASE_DIR+files[-1].split(' ')[-1]+DATA_DIR
        print(f'[X-FTP] {VIS_LOG_BASE_DIR}')
        ftp.cwd(VIS_LOG_BASE_DIR)
        img_data = []
        ftp.dir(img_data.append)
        newlist = [x.split()[-1]  for x in img_data if ".png" in x
                if (int((str(x.split()[-1].split('.')[0])[3:]))%2 == 0)]# if ".png" in x x.split()[-1].split('.')[0][3:]
        print('[X-FTP]',newlist,f"RETR {max(newlist)}")

        with open(f'{max(newlist)}', 'wb') as local_file:
                    ftp.retrbinary(f'RETR {max(newlist)}', local_file.write)
                    print('[X-FTP] Image downloaded successfully....')
        
        with open(f'{max(newlist)}', 'rb') as file: #f'{max(newlist)}', 'rb'
            pub_data = file.read()
            #publishing image as byte array
            
            mqtt.publish('LR-Mate/IMG-Data',bytearray(pub_data),qos=1)
            print('[X-FTP] Image published successfully....')

                

