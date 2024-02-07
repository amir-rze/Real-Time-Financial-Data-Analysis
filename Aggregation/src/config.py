
import os
from dotenv import dotenv_values

config = dotenv_values()

if config.get('MODE') == 'local' :
    KAFKA_BOOTSTRAP_SERVERS = config.get('KAFKA_BOOTSTRAP_SERVERS')
    HOST = config.get('HOST')
    PORT = int(config.get('PORT'))

else:   # Container env
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS') 
    HOST = os.getenv('HOST')
    PORT = int(os.getenv('PORT'))

SIGNAL_KAFKA_TOPIC = "stock-signal"