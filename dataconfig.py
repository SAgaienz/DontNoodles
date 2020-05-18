import configparser, pathlib, os, shutil

config = configparser.ConfigParser()
config.read('datasettings.ini')
bddir= pathlib.Path(config['DataPaths']['datadir']).expanduser()
dst = os.getcwd()

for i in os.listdir(bddir):
    s = os.path.join(bddir, i)
    d = os.path.join(dst, i)
    if os.path.isdir(s):
        shutil.copytree(s, d, False, None)
    else:
        shutil.copy2(s, d)
