import ConfigParser
FilePath='config_files/session.config'
def parse_config():
    Config = ConfigParser.RawConfigParser();
    print Config.read(FilePath);

    print FilePath
    print Config.sections()
    delay = Config.getboolean('CONFIG', 'DELAY')
    hitset = Config.get('CONFIG', 'HITSET')
    recset = Config.get('CONFIG', 'RECSET')
    metrics = Config.get('CONFIG', 'METRICS')
    recsize = Config.get('CONFIG', 'RECSIZE')

    return delay, hitset, recset, metrics, recsize
