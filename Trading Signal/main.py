from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json
import logging
import asyncio
from config import ADDITIONAL_DATA_KAFTA_TOPIC,KAFKA_BOOTSTRAP_SERVERS,SIGNAL_KAFKA_TOPIC,METRICS_KAFKA_TOPIC
from schemas import Signals

logging.basicConfig(level=logging.INFO)

topic_list=[]
topic_list.append(ADDITIONAL_DATA_KAFTA_TOPIC)
topic_list.append(METRICS_KAFKA_TOPIC)


def generate_signal(data) :
    signal = None
    stock_symbol = None 
    if 'rsi' in data:
        stock_symbol = data['stock_symbol']
        ma = data['moving_avg']
        ema = data['exp_moving_avg']
        rsi = data['rsi']
        current_price = data['current_price']
        
        if current_price < ma and rsi < 30 :
            signal = "buy"
        elif current_price > ma and rsi > 70:
            signal = "sell"
        else:
            signal = "hold"
        logging.info("Trading Signal service generated signal based on metrics ! ")

    else:
        if data['data_type'] == "order_book":
            stock_symbol = data['stock_symbol']
            order_type = data['order_type']
            price = data['price']
            quantity = data['quantity']

            if order_type == 'buy' and price < 550 and quantity > 50:
                signal =  'Buy'
            elif order_type == 'sell' and price > 550 and quantity > 50:
                signal = 'Sell'

            logging.info("Trading Signal service generated signal based on order_book ! ")


        elif data['data_type'] == "news_sentiment":
            stock_symbol = data['stock_symbol']
            sentiment_score = data['sentiment_score']
            sentiment_magnitude = data['sentiment_magnitude']

            if sentiment_score > 0 and sentiment_magnitude > 0.5:
                signal = 'Buy'
            elif sentiment_score < 0 and sentiment_magnitude > 0.5:
                signal = 'Sell'

            logging.info("Trading Signal service generated signal based on news_sentiment ! ")

        elif data["data_type"] == "market_data":
            stock_symbol = data['stock_symbol']
            market_cap = data['market_cap']
            pe_ratio = data['pe_ratio']

            if market_cap > 1e11 and pe_ratio < 15:
                signal =  'Buy'
            elif market_cap < 1e10 and pe_ratio > 20:
                signal =  'Sell'

            logging.info("Trading Signal service generated signal based on market_data ! ")

        else:
            stock_symbol = "all"
            indicator_name = data['indicator_name']
            value = data['value']

            if indicator_name == 'GDP Growth Rate' and value > 0:
                signal = 'Buy'
            elif indicator_name == 'GDP Growth Rate' and value < 0:
                signal = 'Sell'

            logging.info("Trading Signal service generated signal based on economic_indicator ! ")

    if signal is not None:
        result = {'signal':signal,'stock_symbol':stock_symbol}
        return Signals(**result)
    else:
        return None


# Define the Kafka producer
async def send_signals(signals: Signals):
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    await producer.start()
    try:
        await producer.send_and_wait(SIGNAL_KAFKA_TOPIC, value=dict(signals))
        logging.info("Trading Signal service sent signal ! ")
    finally:
        await producer.stop()



async def read_data():

    loop = asyncio.get_event_loop()
    consumer = AIOKafkaConsumer(
        *topic_list,loop=loop,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    await consumer.start()
    try:
        async for message in consumer:
            data = message.value
            logging.info("Trading Signal service received data from topics! ")

            signal = generate_signal(data)
            if signal is not None:
                await send_signals(signal)

    finally:
        await consumer.stop()



if __name__ == '__main__':
    asyncio.run(read_data())