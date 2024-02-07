from pydantic import BaseModel
from typing import List
from datetime import datetime
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json
import logging
import numpy as np
import asyncio
from config import KAFKA_BOOTSTRAP_SERVERS,DATA_KAFKA_TOPIC,METRICS_KAFKA_TOPIC,PERIOD
from schemas import Metrics
import pandas as pd

logging.basicConfig(level=logging.INFO)

data_by_symbol = {}
n = PERIOD


# clients = set()


def moving_average(data, n):
    """
    Calculates the moving average of a stock over a specified number of periods.
    """
    return  data['closing_price'].rolling(window=n).mean().iloc[-1].item()

def exponential_moving_average(data, n):
    """
    Calculates the exponential moving average of a stock over a specified number of periods.
    """
    alpha = 0.4
    return data['closing_price'].ewm(span=n, adjust=False).mean().iloc[-1].item()

def relative_strength_index(data, n):
    """
    Calculates the relative strength index of a stock over a specified number of periods.
    """
    delta = data['closing_price'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=n, min_periods=1).mean()
    avg_loss = loss.rolling(window=n, min_periods=1).mean()
    
    # Avoid division by zero by setting RS to a high value if avg_loss is 0
    rs = avg_gain / avg_loss.replace(to_replace=0, value=1e-10)
    
    rsi = 100 - (100 / (1 + rs))
    
    return rsi.iloc[-1].item()

def calculate_metrics(data):
    stock_symbol = data['stock_symbol']
    if stock_symbol not in data_by_symbol:
        data_by_symbol[stock_symbol] = []
    data_by_symbol[stock_symbol].append(data)

    # Calculate the indicators for each stock symbol
    for symbol, data in data_by_symbol.items():
        if n < len(data):
            closing_prices = [d['closing_price'] for d in data]
            current_price = closing_prices[-1]
            closing_prices = closing_prices[:n]
            closing_prices = pd.DataFrame({'closing_price': closing_prices})
            ma = moving_average(closing_prices, n)
            ema = exponential_moving_average(closing_prices, n)
            rsi = relative_strength_index(closing_prices, n)
            print(f"Stock symbol: {symbol}")
            print(f"Moving average: {ma}")
            print(f"Exponential moving average: {ema}")
            print(f"Relative strength index: {rsi}")
            metrics = {
                'stock_symbol' : symbol,
                'moving_avg' : ma,
                'exp_moving_avg':ema,
                'rsi' : rsi , 
                'current_price' : current_price
            }
            data_by_symbol[symbol]=[]
            return Metrics(**metrics)
    return None


# Define the Kafka producer
async def send_metrics(metrics: Metrics):
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    await producer.start()
    try:
        await producer.send_and_wait(METRICS_KAFKA_TOPIC, value=dict(metrics))
        logging.info("Stream Processing service sent metrics ! ")
    finally:
        await producer.stop()


# Define the Kafka consumer
async def read_data():
    loop = asyncio.get_event_loop()
    consumer = AIOKafkaConsumer(
        DATA_KAFKA_TOPIC,loop=loop,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    await consumer.start()
    try:
        async for message in consumer:
            data = message.value
            # await broadcast_realtime_data(data)
            logging.info("Stream Processing service received data ! ")
            metrics = calculate_metrics(data)
            if metrics is not None:
                await send_metrics(metrics)
    finally:
        await consumer.stop()

if __name__ == '__main__':
    asyncio.run(read_data())