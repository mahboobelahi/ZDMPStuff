# Anonymous FTP login
from ftplib import FTP, all_errors
from dateutil import parser
import string

IMG_file = 'pic.png'
VIS_LOG_BASE_DIR = 'ud1:/vision/logs/'#y21oct21/sub00000
DATA_DIR = '/sub00000'
REMOVE_DIR = ''
count=0
with FTP('192.168.1.1') as ftp:
    print(f'[X] Welcom Msg from Robot: {ftp.getwelcome()}')
    # working with directories
    
    print(f'[X] Root_Dir: {ftp.pwd()}')  # Usually default is md:\ memory device
    # with open(IMG_file, 'rb') as image_file:
    #     ftp.storbinary(f'STOR {IMG_file}', image_file)
    #print(ftp.mkd('mydir'))
    # print('Chnging to Vision Dir....')  # Change to fr:,mc:
    ftp.cwd(VIS_LOG_BASE_DIR) #fr:/vision/data
    print(f'[X] Current_Dir: {ftp.pwd()}')
    # #List files

    files = []
    latest_time = None
    latest_name = None
    ftp.dir(files.append)  # Takes a callback for each file
    VIS_LOG_BASE_DIR=VIS_LOG_BASE_DIR+files[-1].split(' ')[-1]+DATA_DIR
    print(f'[X] {VIS_LOG_BASE_DIR}')
    # for f in files:
    #     print(f)
        
        # tokens = f.split()   
        # time_str = tokens[5] + " " + tokens[6] + " " + tokens[7]
        # print(time_str)  
        # if ('y21' or 'y22') in f:
        #     VIS_LOG_BASE_DIR=VIS_LOG_BASE_DIR+f.split(' ')[-1]+DATA_DIR
        #     REMOVE_DIR = f.split(' ')[-1]
        #     print(VIS_LOG_BASE_DIR) #.split(' ')
    # try:
    #     ftp.rmd('ud1:/vision/log/y21oct20/sub00000')
    # except all_errors as error:
    #     print(f'Error deleting file: {error}') 
    # # File size method not working
    # try:
    #     ftp.sendcmd('TYPE I')  # "ASCII" text
    #     print(ftp.size('pic.png'))
    # except all_errors as error:
    #     print(f"Error checking text file size: {error}")

    ftp.cwd(VIS_LOG_BASE_DIR)
    img_data = []
    ftp.dir(img_data.append)
    #print(img_data)
    newlist = [x.split()[-1]  for x in img_data if ".png" in x if (int((str(x.split()[-1].split('.')[0])[3:]))%2 == 0)]# if ".png" in x x.split()[-1].split('.')[0][3:]
    print('[X]',newlist,f"RETR {max(newlist)}")
    #print(f'[X] {img_data.split()[-1]}')
    with open(f'{max(newlist)}', 'wb') as local_file:
                 ftp.retrbinary(f'RETR {max(newlist)}', local_file.write)
                 print('[X] Image downloaded successfully....')
    # ftp.cwd(VIS_LOG_BASE_DIR)
    # files.clear()
    # ftp.dir(files.append)  # Takes a callback for each file
    # print(len(files))
    # for f in files:
    #     if ('.png') in f.split(' ')[-1]:
    #         count=count+1
    #         with open(f'image{count}.png', 'wb') as local_file:
    #             ftp.retrbinary(f"RETR {f.split(' ')[-1]}", local_file.write)
                

