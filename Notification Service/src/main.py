import socket
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json
import logging
import asyncio
from config import KAFKA_BOOTSTRAP_SERVERS,SIGNAL_KAFKA_TOPIC,DATA_KAFKA_TOPIC,HOST,PORT

clients = set()

topic_list=[]
topic_list.append(DATA_KAFKA_TOPIC)
topic_list.append(SIGNAL_KAFKA_TOPIC)

logging.basicConfig(level=logging.INFO)


async def client_handler(reader, writer):
    clients.add(writer)
    try:
        while True:
            # Here, you could add logic to receive data from the client if needed
            await asyncio.sleep(1)  # Prevent the loop from closing immediately
    except asyncio.CancelledError:
        pass
    finally:
        clients.remove(writer)
        writer.close()
        await writer.wait_closed()

async def broadcast_data(data):
    for writer in list(clients):
        try:
            writer.write(json.dumps(data).encode('utf-8'))
            await writer.drain()
            logging.info("Data sent to client!")
        except :
            clients.remove(writer)
            writer.close()
            logging.info("Client connection closed.")


async def read_data():
    consumer = AIOKafkaConsumer(
        *topic_list,
        loop=asyncio.get_event_loop(),
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    await consumer.start()
    try:
        async for message in consumer:
            data = message.value
            logging.info("Notification Service received data!")
            await broadcast_data(data)
    finally:
        await consumer.stop()

async def start_server(host, port):
    server = await asyncio.start_server(client_handler, host, port)
    logging.info(f'Server is listening on {port}...')
    async with server:
        await server.serve_forever()

async def main():
    await asyncio.gather(
        start_server(HOST, PORT),
        read_data(),
    )

if __name__ == '__main__':
    asyncio.run(main())