import configparser

def read_ini(file_path, flag):
    port = 0
    config = configparser.ConfigParser()
    config.read(file_path)
    for section in config.sections():
        for key in config[section]:
            if (key == 'async_port' and flag == 'asyncio') or (key == 'twist_port' and flag == 'twisted'):
                port = int(config[section][key])
    return port