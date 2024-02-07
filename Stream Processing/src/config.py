import os
from dotenv import dotenv_values

config = dotenv_values()


# calculating period
PERIOD = 7


if config.get('MODE') == 'local' :
    KAFKA_BOOTSTRAP_SERVERS = config.get('KAFKA_BOOTSTRAP_SERVERS')

else:   # Container env
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS') 

METRICS_KAFKA_TOPIC  = "stock-metrics"
DATA_KAFKA_TOPIC = "stock-data"