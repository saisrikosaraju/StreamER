import ConfigParser
def parse_config(FilePath):
    Config = ConfigParser.RawConfigParser();

    #Read Configuration File
    Config.read(FilePath)

    hitset = Config.get('CONFIG', 'HITSET')
    recset = Config.get('CONFIG', 'RECSET')
    metrics = Config.get('CONFIG', 'METRICS')
    recsize = Config.get('CONFIG', 'RECSIZE')
    algorithms = Config.get('CONFIG', 'ALGORITHMS')

    return hitset, recset, metrics, recsize, algorithms
