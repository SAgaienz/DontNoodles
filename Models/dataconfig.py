import configparser, pathlib

config = configparser.ConfigParser()
config.read('config.ini')
datadir = pathlib.Path(config['Paths']['bulkdir']).expanduser()

