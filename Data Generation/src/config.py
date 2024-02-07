import os
from dotenv import dotenv_values

config = dotenv_values()



if config.get('MODE') == 'local' :
    HOST = config.get('HOST')
    PORT = config.get('PORT')

else:   # Container env
    HOST = os.getenv('HOST') 
    PORT = os.getenv('PORT')
