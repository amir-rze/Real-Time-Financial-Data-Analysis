from fastapi import FastAPI, HTTPException,Depends,Request,status,WebSocket
from fastapi_cache import FastAPICache
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


logging.basicConfig(level=logging.INFO)

connected_clients = set()

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
        # Added try except
        try:
            data=dict(data)
            score = data['timestamp'].timestamp()
            data['timestamp'] = convert_utc_to_Tehran(data['timestamp'])
            db_data = Data(**data)
            db.add(db_data)
            db.commit()

            data['timestamp'] = convert_datetime_to_str(data['timestamp'])
            redis_client.zadd("data", {json.dumps(data): score})
            # Remove records older than one hour
            one_hour_ago = datetime.now() - timedelta(hours=1)
            redis_client.zremrangebyscore("data", 0, one_hour_ago.timestamp())
            logging.info("Data Ingestion service stored data in database ! ")
            await send_data(data,DATA_KAFKA_TOPIC)
            for client in list(connected_clients):
                await client.send_json(data)
                logging.info("data sent to client successfully...")

            return {"status" : 200 ,"message": "Data ingested successfully"}
        # Added try-except clause    
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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    

# Define the route to retrieve the data for the past hour
@app.get("/data/", response_model=List[DataOut])
async def read_data(db: Session = Depends(get_db)):
    # Fetch all data from Redis
    data = await redis_client.zrange("data", 0, -1)
    return [json.loads(d) for d in data]



FastAPICache.init(RedisBackend(redis_client), prefix="data-ingestion-service")


