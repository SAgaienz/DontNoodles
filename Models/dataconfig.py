import configparser, pathlib, os
from sys import platform


config = configparser.ConfigParser()
if os.path.exists(r'/home/sagaienz/Internal/UserData/Documents/ChemEng/CSC/CSC411 Source Code Repo/Models/config.ini'):
    config.read(r'/home/sagaienz/Internal/UserData/Documents/ChemEng/CSC/CSC411 Source Code Repo/Models/config.ini')   

    if platform == "linux":
        datadir = pathlib.Path(config['PathLinux']['bulkdir']).expanduser()
    if platform == "win32":
        datadir = pathlib.Path(config['PathWin']['bulkdir']).expanduser()
    if platform == "darwin":
        datadir = pathlib.Path(config['PathMac']['bulkdir']).expanduser()
    print('Current Data dir is "' + str(datadir)+'"')
    print('OS: ' + str(platform))
else:
    print('File "config.ini" cannot be found')
