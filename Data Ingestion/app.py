from fastapi import FastAPI, HTTPException,Depends,Request,status,WebSocket
from fastapi_cache import FastAPICache
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache.backends.redis import RedisBackend
import json
from typing import List
from datetime import datetime, timedelta
import redis
from aiokafka import AIOKafkaProducer
from database import engine,SessionLocal,Base
from sqlalchemy.orm import Session
from models import Data
from schemas import DataIn,DataOut,AdditionalDataInEconomic,AdditionalDataInMarket,AdditionalDataInNews,AdditionalDataInOrder
from utils import convert_datetime_to_str,convert_utc_to_Tehran
from typing import Union
import logging

from config import KAFKA_BOOTSTRAP_SERVERS,DATA_KAFKA_TOPIC,REDIS_URL,LOOP,ADDITIONAL_DATA_KAFTA_TOPIC


# Create the tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


# Configure CORS
origins = [
    "*"  # The origin of your frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

logging.basicConfig(level=logging.INFO)

connected_clients = []

# Create the Redis client
redis_client = redis.Redis.from_url(REDIS_URL)


def get_db() :
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Define the Kafka producer
async def send_data(data,topic):
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,loop=LOOP,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    await producer.start()
    try:
        await producer.send(topic, value=data)
        logging.info("data or additional-data sent to stream processing service successfully...")
    except Exception as e:
        logging.error("Failed to send data or additional data")
    finally: 
        await producer.stop()



# Define the route to receive the data
@app.post("/ingest/",status_code=status.HTTP_200_OK)
async def ingest_data(
     data: Union[DataIn, AdditionalDataInOrder, AdditionalDataInNews, AdditionalDataInMarket, AdditionalDataInEconomic] ,
      db: Session = Depends(get_db)):
    
    if isinstance(data, DataIn):
<<<<<<< HEAD
        # Added try except
=======
>>>>>>> 12dd70abc317f906748e27395d37be8667dc3127
        try:
            data=dict(data)
            data['timestamp'] = convert_utc_to_Tehran(data['timestamp'])
            db_data = Data(**data)
            db.add(db_data)
            db.commit()
            logging.info("Data Ingestion service stored data in database ! ")
            score = data['timestamp'].timestamp()
            data['timestamp'] = convert_datetime_to_str(data['timestamp'])
            redis_client.zadd(f"data:{data['stock_symbol']}", {json.dumps(data): score})
            # Remove records older than one hour
            one_hour_ago = datetime.now() - timedelta(hours=1)
            redis_client.zremrangebyscore(f"data:{data['stock_symbol']}", 0, one_hour_ago.timestamp())
            logging.info("Data stored in Redis database ! ")
            await send_data(data,DATA_KAFKA_TOPIC)
            return {"status" : 200 ,"message": "Data ingested successfully"}
<<<<<<< HEAD
        # Added try-except clause    
=======
>>>>>>> 12dd70abc317f906748e27395d37be8667dc3127
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            db.close()
    elif isinstance(data, AdditionalDataInOrder) or isinstance(data, AdditionalDataInNews)\
            or isinstance(data, AdditionalDataInMarket) or isinstance(data, AdditionalDataInEconomic) :
        data = dict(data)
        data['timestamp'] = convert_datetime_to_str(data['timestamp'])
        await send_data(data,ADDITIONAL_DATA_KAFTA_TOPIC)
        return {"status" : 200 ,"message": "Data ingested successfully"}
    else:
        return {"status" : 400 , "message": "Data is not valid!"}


# Define the route to retrieve the data for the past hour
@app.get("/data/", response_model=List[DataOut])
def read_data(stock: str, db: Session = Depends(get_db)):
    # Fetch data for the specified stock_symbol from Redis
    data =  redis_client.zrange(f"data:{stock}", 0, -1)
    return [json.loads(d) for d in data]



FastAPICache.init(RedisBackend(redis_client), prefix="data-ingestion-service")


