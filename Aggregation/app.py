from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json
import logging
import asyncio
from typing import List
from fastapi import FastAPI, HTTPException,Depends,Request,status
from sqlalchemy.orm import Session

from config import KAFKA_BOOTSTRAP_SERVERS,SIGNAL_KAFKA_TOPIC
from models import Summary
from database import Base , SessionLocal,engine
from schemas import SummaryOut
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)


# Create the tables
Base.metadata.create_all(bind=engine)


def get_db() :
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def update_database(data):
    db = SessionLocal()
    record = db.query(Summary).filter(Summary.stock_symbol == data['stock_symbol']).first()
    if record:
        if data['signal'] == 'Sell':
            record.sell_count += 1
        elif data['signal'] == 'Buy':
            record.buy_count += 1
        db.commit()
        logging.info("a record updated in Summary table ! ")
    else:
        # Create a new record
        new_record = Summary(stock_symbol=data['stock_symbol'], sell_count=0, buy_count=0)
        if data['signal'] == 'Sell':
            new_record.sell_count = 1
        elif data['signal'] == 'Buy':
            new_record.buy_count = 1
        db.add(new_record)
        db.commit()
        logging.info("new record added to Summary table ! ")

    return


async def read_data():

    loop = asyncio.get_event_loop()
    consumer = AIOKafkaConsumer(
        SIGNAL_KAFKA_TOPIC,loop=loop,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    await consumer.start()
    try:
        async for message in consumer:
            data = message.value
            logging.info("Aggregation service received data ! ")
            await update_database(data)
    finally:
        await consumer.stop()


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(read_data())
    logging.info("Aggregation service received data !")    
    yield

app = FastAPI(lifespan=lifespan)

# Configure CORS
origins = [
    "http://localhost:3000",  # The origin of your frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/summary/", response_model=List[SummaryOut])
async def get_summaries(db: Session = Depends(get_db)):
    summaries = db.query(Summary).all()
    logging.info("Stock summary sent to client ! ")
    return summaries

