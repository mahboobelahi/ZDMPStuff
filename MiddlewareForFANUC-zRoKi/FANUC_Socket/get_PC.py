# Anonymous FTP login
from ftplib import FTP, all_errors
from dateutil import parser


with FTP('192.168.1.1') as ftp:
    print(f'[X] Welcom Msg from Robot: {ftp.getwelcome()}')
    # working with directories

    # Usually default is md:\ memory device
    print(f'[X] Root_Dir: {ftp.pwd()}')
    ftp.cwd('UD1:')  # fr:/vision/data
    print(f'[X] Current_Dir: {ftp.pwd()}')
    files = []
    ftp.dir(files.append)  # Takes a callback for each file
    for f in files:
        if 'vision' in f:

            print(f'[X] {f}')  # {f.split()[-1]}
